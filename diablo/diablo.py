"""
Diablo

NetworkX Query Language: Based on Gremlin
https://tinkerpop.apache.org/gremlin.html

"""

class Diablo():
    """
    diablo: gremlin-like networkx tool

    parameters:
    - graph: the graph to query and traverse
    """

    def __init__(self, graph, active_nodes=None):
        self.graph = graph
        if active_nodes:
            self.active_nodes = active_nodes
        else:
            # select everything
            self.active_nodes = graph.nodes()
        self.cached_nodes = None

    def __get_cached_nodes(self):
        """
        Get the nodes which are referenced by the cursor
        """
        if not self.cached_nodes:
            self.cached_nodes = [(x,y) for x,y in self.graph.nodes(data=True) if x in self.active_nodes]
        return self.cached_nodes

    def has(self, key, value):
        """
        'has' filters graphs by a key/value attribute pairs on nodes.

        parameters:
        - key: node attribute name to filter on
        - value: node attribute value to filter on

        returns diablo instance to enable function chaining
        """
        active_nodes = [x for x,y in self.graph.nodes(data=True) if y.get(key) == value]
        newd = Diablo(self.graph, active_nodes)
        return newd

    def out(self, *relationship, key='relationship'):
        """
        'out' traverses a graph by following edges with the passed relationship.

        parameters:
        - relationsip(s): traverses node following edges with the stated relationship
        - key: sets the key which defines the relationship attribute

        returns diablo instance to enable function chaining
        """
        active_nodes = [y for x,y,e in self.graph.edges(data=True) if x in self.active_nodes and e.get(key) in relationship]
        newd = Diablo(self.graph, active_nodes)
        return newd

    def values(self, key):
        """
        'values' returns a list of values of the selected nodes.

        parameters:
        - key: the attribute to read the value from 

        returns a list of values
        """
        return list(set([y.get(key) for x,y in self.__get_cached_nodes()]))

    def groupCount(self, key):
        """
        'groupCount' counts nodes per key attribute

        parameters:
        - key: key to group by

        returns a dictionary of counts
        """
        from collections import Counter
        nodes = Counter([y.get(key) for x,y in self.__get_cached_nodes()])
        return dict(nodes)

    def _is(self, *identity):
        """
        'is' selects a single node.

        parameters:
        - identity(s): the identity of the node to select

        returns diablo instance to enable function chaining
        """
        active_nodes = []
        for ident in identity:
            if ident in self.graph.nodes():
                active_nodes.append(ident)
        newd = Diablo(self.graph, ident)
        return newd

    def nodes(self, data=False):
        """
        Returns the nodes currently selected
        """
        if data:
            return self.__get_cached_nodes()
        return [x for x in self.graph.nodes() if x in self.active_nodes]

    def edges(self, data=False):
        """
        Returns all edges of the base graph
        """
        return self.graph.edges(data=data)

    def __len__(self):
        return len(self.active_nodes)

    def __str__(self):
        return "diablo object"
