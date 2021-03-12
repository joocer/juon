import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from diablo import Graph
from graph_data import build_graph

def test_graph():

    graph = build_graph()

    # are the node and edge counts right?
    assert len(graph.nodes()) == 10
    assert len(list(graph.edges())) == 14

    nodes = graph.nodes(data=True)
    edges = list(graph.edges())



def test_outgoing_edges():

    graph = build_graph()

    outgoing = graph.outgoing_edges('Sharlene')

    assert len(outgoing) == 3
    
    sources = [s for s,t,r in outgoing]
    targets = [t for s,t,r in outgoing]
    relationships = [r for s,t,r in outgoing]

    assert set(sources) == {'Sharlene'}
    assert sorted(targets) == ['Bindoon', 'Ceanne', 'Lainie']
    assert sorted(relationships) == ['Daughter', 'Lives In', 'Sister']

def test_epitomize():

    graph = build_graph()

    summ = graph.epitomize()
    # are the node and edge counts right?
    assert len(summ.nodes()) == 3
    assert len(list(summ.edges())) == 5

    assert sorted(summ.nodes()) == ['Locality', 'Person', 'Restaurant']

if __name__ == "__main__":

    test_graph()
    test_outgoing_edges()
    test_epitomize()
