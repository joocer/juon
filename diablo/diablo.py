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

class Diablo():
    """
    diablo: gremlin-like networkx tool

    parameters:
    - graph: the graph to query and traverse
    """

    def __init__(self, graph):
        self.graph = graph
        self.cursor = graph.nodes()

    def has(self, key, value):
        """
        'has' filters graphs by a key/value attribute pairs on nodes.

        parameters:
        - key: node attribute name to filter on
        - value: node attribute value to filter on

        returns diablo instance to enable function chaining
        """
        cursor = [x for x,y in self.graph.nodes(data=True) if y.get(key) == value]
        newd = Diablo(self.graph)
        newd.cursor = cursor
        return newd

    def out(self, relationship, key='relationship'):
        """
        'out' traverses a graph by following edges with the passed relationship.

        parameters:
        - relationsip: traverses node following edges with the stated relationship
        - key: sets the key which defines the relationship attribute

        returns diablo instance to enable function chaining
        """
        cursor = [y for x,y,e in self.graph.edges(data=True) if x in self.cursor and e.get(key) == relationship]
        newd = Diablo(self.graph)
        newd.cursor = cursor
        return newd

    def values(self, key):
        """
        'values' returns a list of values of the selected nodes.

        parameters:
        - key: the attribute to read the value from 

        returns a list of values
        """
        return [y.get(key) for x,y in self.graph.nodes(data=True) if x in self.cursor]

    def hasLabel(self, label):
        raise NotImplementedError()

    def label(self):
        raise NotImplementedError()

    def groupCount(self):
        raise NotImplementedError()

    def inE(self, key):
        raise NotImplementedError()

    def nodes(self, data=False):
        """
        Returns the nodes currently selected
        """
        if data:
            return [(x,y) for x,y in self.graph.nodes(data=data) if x in self.cursor]
        return [x for x in self.graph.nodes() if x in self.cursor]

    def edges(self, data=False):
        """
        Returns all edges of the base graph
        """
        return self.graph.edges(data=data)

    def __len__(self):
        return len(self.cursor)

