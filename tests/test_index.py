import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))


def test_index():
    from diablo.index import BPlusTree

    b = BPlusTree(order=16)
    words = [
            'Serendipity',
            'Petrichor',
            'Supine',
            'Solitude',
            'Aurora',
            'Idyllic',
            'Clinomania',
            'Pluviophile',
            'Euphoria',
            'Sequoia']

    for word in words:
        b.insert(word[:1], word)

    k = [k for k,v in b.items()]
    v = [v for k,v in b.items()]

    # we should have 10 keys in alphabetical order
    assert len(k) == 10
    assert k == ['A', 'C', 'E', 'I', 'P', 'P', 'S', 'S', 'S', 'S']

    # we should have 10 values in alphabetical order
    assert len(v) == 10
    assert v == ['Aurora', 'Clinomania', 'Euphoria', 'Idyllic', 'Petrichor', 'Pluviophile', 'Serendipity', 'Supine', 'Solitude', 'Sequoia']

    # we should have 6 keys (deduplicated) in alphabetical order
    assert list(b.keys()) == ['A', 'C', 'E', 'I', 'P', 'S']


if __name__ == "__main__":
    test_index()

    print('okay')
