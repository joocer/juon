import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from data_sets import words_10, albums_25, words_10_ordered
from diablo import Index

def test_read_file():

    index = Index.read_file('tests/imdb.index')

    k = [k for k,v in index.items()]
    v = [v for k,v in index.items()]

    # we should have 250 keys, we're not going to test them all
    assert len(k) == 250
    assert min(k) == k[0]
    assert max(k) == k[len(k) - 1]

    # we should have 250 values
    assert len(v) == 250
    assert v[0] == "The Kid"
    assert v[249] == "Soul"

    # the .keys should be the unique set from the k variable able
    assert len(list(index.keys())) == len(set(k))

    # test some years
    assert index.retrieve('1977') == ['Star Wars']
    assert index.retrieve('1999') == ['Fight Club', 'The Matrix', 'The Green Mile', 'American Beauty', 'The Sixth Sense']

if __name__ == "__main__":
    test_read_file()

    print('okay')
