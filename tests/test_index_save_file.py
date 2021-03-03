import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from data_sets import words_10, albums_25, words_10_ordered
from diablo import Index

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from data_sets import words_10, albums_25, words_10_ordered
from diablo import Index

def test_save_index():

    keys = [word[:1] for word in words_10_ordered]
    pre_save_index = Index.bulk_load(keys, words_10_ordered, order=2)
    pre_save_index.save('save.index')

    post_save_index = Index.read_file('save.index')

    k = [k for k,v in post_save_index.items()]
    v = [v for k,v in post_save_index.items()]

    # we should have 10 keys in alphabetical order
    assert len(k) == 10
    assert k == ['A', 'C', 'E', 'I', 'P', 'P', 'S', 'S', 'S', 'S']

    # we should have 10 values in alphabetical order
    assert len(v) == 10
    assert v == ['Aurora', 'Clinomania', 'Euphoria', 'Idyllic', 'Petrichor', 'Pluviophile', 'Serendipity', 'Supine', 'Solitude', 'Sequoia']

    # we should have 6 keys (deduplicated) in alphabetical order
    assert list(post_save_index.keys()) == ['A', 'C', 'E', 'I', 'P', 'S']


if __name__ == "__main__":
    test_save_index()

    print('okay')
