"""
Diablo

NetworkX Query Language: Based on Gremlin
https://tinkerpop.apache.org/gremlin.html


gremlin> g.V().label().groupCount()
==>[occupation:21, movie:3883, category:18, user:6040]

gremlin> g.V().hasLabel('movie').values('year').min()
==>1919

gremlin> g.V().has('movie','name','Die Hard').inE('rated').values('stars').mean()
==>4.121848739495798
"""

class diablo():

    def __init__(self, graph):
        self.graph = graph
        self.cursor = graph.nodes()

    def has(self, key, value):
        # return diablo instance
        cursor = [x for x,y in self.graph.nodes(data=True) if y.get(key) == value]
        newd = diablo(self.graph)
        newd.cursor = cursor
        return newd

    def out(self, relationship):
        # return diable instance
        cursor = [y for x,y,e in self.graph.edges(data=True) if x in self.cursor and e.get('relationship') == relationship]
        newd = diablo(self.graph)
        newd.cursor = cursor
        return newd

    def values(self, key):
        # return list of values
        return [y.get('label') for x,y in self.graph.nodes(data=True) if x in self.cursor]

    def nodes(self, data=False):
        # these are the nodes which are selected by cursor
        if data:
            return [(x,y) for x,y in self.graph.nodes(data=data) if x in self.cursor]
        return [x for x in self.graph.nodes() if x in self.cursor]

    def edges(self, data=False):
        # this always return
        return self.graph.edges(data=data)

    def __len__(self):
        return len(self.cursor)




import networkx as nx

g = nx.read_graphml('graph/mitre-data.graphml')
d = diablo(g)

print(len(g.nodes()), len(g.edges()))
h = d.has('section_id', 'V14').out('Prevents').values('node_type')
print(len(h))
print(h)
