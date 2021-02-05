"""
Diablo: Graph Query Language: Based on Gremlin
https://tinkerpop.apache.org/gremlin.html

(C) 2021 Justin Joyce.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

class Diablo(object):

    __slots__ = ('graph', 'active_nodes', 'cached_active_nodes', 'nodes_cache')

    def __init__(
            self,
            graph,
            active_nodes: set = (),
            nodes_cache = None):
        """
        Diablo: A Graph Query Language

        Parameters:
        - graph: the graph to query and traverse
        - active_nodes: the nodes which are selected for this instance
        """
        self.graph = graph

        if len(active_nodes) > 0:
            # ensure it is a set
            # - the collection active nodes is immutable
            # - sets are faster for look ups 
            if type(active_nodes).__name__ == 'set':
                self.active_nodes = active_nodes
            else:
                self.active_nodes = set(active_nodes)
        else:
            # select everything from the base graph
            self.active_nodes = set(graph.nodes())
        
        # create the variable but don't fill it until used
        self.cached_active_nodes = None
        self.nodes_cache = nodes_cache

    def V(self, *nodes):
        """
        Initialize Diablo against a graph.
        """ 
        self.nodes_cache = self.graph.nodes(data=True)
        return self._is(*nodes)

    def _get_cached_active_nodes(self):
        """
        Get the nodes which are referenced by the cursor
        """
        if not self.cached_active_nodes:
            self.cached_active_nodes = {x:y for x,y in self.nodes_cache if x in self.active_nodes}
        return self.cached_active_nodes

    def has(self, key: str, value: str):
        """
        'has' filters graphs by a key/value attribute pairs on nodes.

        parameters:
        - key: node attribute name to filter on
        - value: node attribute value to filter on

        returns: new Diablo instance
        """
        active_nodes = {x for x,y in self.nodes_cache if y.get(key) == value}
        return Diablo(self.graph, active_nodes, self.nodes_cache)

    def out(self, *relationship):
        """
        'out' traverses a graph by following edges with the passed relationship.

        parameters:
        - relationsip(s): traverses node following edges with the stated relationship
        - key: sets the key which defines the relationship attribute

        returns diablo instance to enable function chaining
        """
        active_nodes = []
        for rel in relationship:
            edges = self.graph._edges.get(rel, {})
            active_nodes += [y for x,y in edges if x in self.active_nodes]
        return Diablo(self.graph, active_nodes, self.nodes_cache)

    def values(self, key):
        """
        'values' returns a list of values of the selected nodes.

        Parameters:
        - key: the attribute to read the value from 

        returns a list of values
        """
        return list({y.get(key) for x,y in self._get_cached_active_nodes().items()})

    def groupCount(self, key):
        """
        'groupCount' counts nodes per key attribute

        Parameters:
        - key: key to group by

        returns: a dictionary of counts
        """
        from collections import Counter
        nodes = Counter([y.get(key) for x,y in self._get_cached_active_nodes().items()])
        return dict(nodes)

    def _is(self, *identity):
        """
        'is' explicitly selects nodes.

        Parameters:
        - identity(s): the identity(s) of the node(s) to select

        Returns:
            A new Diablo instance
        """
        identity_set = set(identity)
        active_nodes = [ident for ident in self.graph.nodes() if ident in identity_set]
        return Diablo(self.graph, active_nodes, self.nodes_cache)

    def nodes(self, data=False):
        """
        Returns the currently selected nodes
        """
        if data:
            return [y for x,y in self._get_cached_active_nodes().items()]
        return self.active_nodes

    def edges(self, data=False):
        """
        Returns all edges of the base graph
        """
        result = []
        for rel in self.graph._edges:
            result += self.graph._edges[rel]
        return result

    def __len__(self):
        return len(self.active_nodes)

    def __str__(self):
        return F"Diablo with {len(self.active_nodes)} selected nodes"
