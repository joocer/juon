
import networkx as nx
from  diablo import Diablo

g = nx.read_graphml('graph/mitre-data.graphml')
d = Diablo(g)

print(len(g.nodes()), len(g.edges()))
h = d.has('section_id', 'V14').out('Prevents').values('label')
print(len(h))
#print(h.nodes(data=True))
print(h)
