"""
Diablo: Python Graph Library

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

    __slots__ = ('graph', 'active_nodes')

    def __init__(
            self,
            graph,
            active_nodes: set = ()):
        """
        Diablo: A Graph Query Language

        Parameters:
        - graph: the graph to query and traverse
        - active_nodes: the nodes which are selected for this instance
        """
        self.graph = graph

        if active_nodes:
            # ensure it is a set
            # - the collection active nodes is immutable
            # - sets are faster for look ups 
            if type(active_nodes).__name__ == 'set':
                self.active_nodes = active_nodes
            else:
                self.active_nodes = set(active_nodes)
        else:
            #print('loading everything')
            # select everything from the base graph
            self.active_nodes = set(graph.nodes())

    def V(self, *nodes):
        """
        Initialize Diablo against a graph.
        """ 
        #self.nodes_cache = self.graph.nodes(data=True)
        return self._is(*nodes)

    def has(self, key: str, value: str):
        """
        'has' filters graphs by a key/value attribute pairs on nodes.

        parameters:
        - key: node attribute name to filter on
        - value: node attribute value to filter on

        returns: new Diablo instance
        """
        #print(F'has({key}, {value})')
        active_nodes = [x for x,y in self.graph.nodes(data=True) if key in y and y[key] == value]
        #print(len(active_nodes))
        return Diablo(self.graph, active_nodes)


    def out(self, *relationship):
        """
        'out' traverses a graph by following edges with the passed relationship.

        parameters:
        - relationsip(s): traverses node following edges with the stated relationship
        - key: sets the key which defines the relationship attribute

        returns diablo instance to enable function chaining
        """
        active_nodes = []

        for node in self.active_nodes:
            active_nodes += [target for target, attribs in self.graph.outgoing_edges(node) if attribs['relationship'] in relationship]

        return Diablo(self.graph, active_nodes)


    def values(self, key):
        """
        'values' returns a list of values of the selected nodes.

        Parameters:
        - key: the attribute to read the value from 

        returns a list of values
        """
        return list({y.get(key) for x,y in self.graph.nodes(data=True) if x in self.active_nodes})

        #nodes = self.nodes()
        #return {node.get(key) for node in nodes}

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
        print('<<', identity)
        print('**', list(self.graph.nodes()))
        active_nodes = [ident for ident in self.graph.nodes() if ident in identity]
        print('>>', active_nodes)
        return Diablo(self.graph, active_nodes)

    def nodes(self, data=False):
        """
        Returns the currently selected nodes
        """
        if data:
            fetch = self.graph._nodes.retrieve
            result = []
            for item in [fetch(node) for node in self.active_nodes]:
                result.append(item)
            return result
        return self.active_nodes

    def edges(self, data=False):
        """
        Returns all edges of the base graph
        """
        return self.graph.edges(data=data)

    def __len__(self):
        return len(self.active_nodes)

    def __str__(self):
        return F"Graph with {len(self.active_nodes)} selected nodes"
