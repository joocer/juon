"""



Adapted from http://pts.github.io/pts-line-bisect/line_bisect_evolution.html

License: GNU GPL v2 or newer, at your choice.
Accessed: 2020-03-06
"""


import ujson as json
from functools import lru_cache


@lru_cache(16)
def _read_and_compare(ofs, f, size, tester):
    """Read a line from f at ofs, and test it.

    Finds out where the line starts, reads the line, calls tester with
    the line with newlines stripped, and returns the results.

    If ofs is in the middle of a line in f, then the following line will be
    used, otherwise the line starting at ofs will be used. (The term ``middle''
    includes the offset of the trailing '\\n'.)

    Bytes of f after offset `size' will be ignored. If a line spans over
    offset `size', it gets read fully (by f.readline()), and then truncated.

    If the line used starts at EOF (or at `size'), then tester won't be not
    called, and True is used instead.

    A cache of previous offsets and test results is read and updated. The size of
    the cache is bounded (it contains at most 4 offsets and 2 test results).

    Args:
        ofs: The offset in f to read from. If ofs is in the middle of a line, then
        the following line will be used.
        f: Seekable file object or file-like object to read from. The methods
        f.tell(), f.seek(ofs_arg) and f.readline() will be used.
        size: Size limit for reading. Bytes in f after offset `size' will be
        ignored.
        tester: Single-argument callable which will be called for the line, with
        the trailing '\\n' stripped. If the line used is at EOF, then tester
        won't be called and True will be used as the result.
    Returns:
        List or tuple of the form [fofs, g, dummy], where g is the test result
        (or True at EOF), fofs is the start offset of the line used in f,
        and dummy is an implementation detail that can be ignored.
    """
    if ofs:
        if f.tell() != ofs - 1:  # Avoid lseek(2) call if not needed.
            f.seek(ofs - 1)  # Just to figure out where our line starts.
        f.readline()  # Ignore previous line, find our line.
        fofs = min(size, f.tell())
    else:
        fofs = 0

    g = True  # EOF is always larger than any line we search for.
    if fofs < size:
        if not fofs and f.tell():
            f.seek(0)
        line = f.readline()  # We read at f.tell() == fofs.
        line = json.loads(line)
        line = str(line.get('key')) 
        if line:
            g = tester(line.rstrip('\n'))

    return [fofs, g, ofs]  # Return the most recent item of the cache.


def bisect_way(f, x, is_left, size=None):
    """Return an offset where to insert line x into sorted file f.

    Bisection (binary search) on newline-separated, sorted file lines.
    If you use sort(1) to sort the file, run it as `LC_ALL=C sort' to make it
    lexicographically sorted, ignoring locale.

    If there is no trailing newline at the end of f, and the returned offset is
    at the end of f, then don't forget to append a '\\n' before appending x.

    Args:
        f: Seekable file object or file-like object to search in. The methods
        f.tell(), f.seek(ofs_arg) and f.readline() will be used.
        x: Line to search for. Must not contain '\\n', except for maybe a
        trailing one, which will be ignored if present.
        is_left: If true, emulate bisect_left. See the return value for more info.
        size: Size limit for reading. Bytes in f after offset `size' will be
        ignored. If None, then no limit.
    Returns:
        Byte offset in where where to insert line x. If is_left is true (i.e.
        bisect_left), then the smallest possible offset is returned, otherwise
        (i.e. bisect_right) the largest possible address is returned.
    """
    f.seek(0, 2)
    size = f.tell()
    if is_left:
        tester = x.__le__  # x <= y.
    else:
        tester = x.__lt__  # x < y.
    lo, hi, mid = 0, size - 1, 1
    while lo < hi:
        mid = (lo + hi) >> 1
        midf, g, _ = _read_and_compare(mid, f, size, tester)
        if g:
            hi = mid
        else:
            lo = mid + 1
        if mid != lo:
            midf = _read_and_compare(lo, f, size, tester)[0]
    return midf


#from btree import BTree
#from files import read_jsonl
#
#r = read_jsonl('twitter.jsonl')
#b = BTree(order=16)
#for i in r:
#    b.insert(i['user_name'], i)
#b.save('sorted_twitter.index')


import sys
import time

def binary(value):
    with open('sorted_twitter.index', 'r') as f:
        start = bisect_way(f, value, True)
        f.seek(start)
        data = f.read(min(1024, 1024)).splitlines()[0]
        return data
        #sys.stdout.write(data + '\n')

def scan(value):
    with open('sorted_twitter.index', 'r') as f:
        for r in f:
            j = json.loads(r)
            if j["key"] == value:
                return r
                #sys.stdout.write(r)

value = '~~k~~'

t = time.time_ns()
for rep in range(100):
    r = binary(value)
print('binary', (time.time_ns() - t) / 1e9, r)

t = time.time_ns()
#for rep in range(100):
#    r = scan(value)
print('scan', (time.time_ns() - t) / 1e9, r)