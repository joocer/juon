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

class Diablo():

    __slots__ = ('graph', '_active_nodes')

    def __init__(
            self,
            graph,
            active_nodes: set = ()):
        """
        Diablo: Graph Traversal
        """
        self.graph = graph

        if active_nodes:
            # ensure it is a set
            # - the collection active nodes is immutable
            # - sets are faster for look ups 
            if type(active_nodes).__name__ == 'set':
                self._active_nodes = active_nodes
            else:
                self._active_nodes = set(active_nodes)
        else:
            #print('loading everything')
            # select everything from the base graph
            self._active_nodes = set(graph.nodes())


    def __len__(self):
        return len(self._active_nodes)


    def follow(self, *relationships):
        """
        Traverses a graph by following edges with relationship matching
        on on the list of relationships.

        Parameters:
            relationsips: strings
                traverses node following edges with the stated relationship
        
        Returns:
            A new Graph instance to enable function chaining
        """
        active_nodes = []

        for node in self._active_nodes:
            active_nodes += [t for (s, t, r) in self.graph.outgoing_edges(node) if r in relationships]
        return Diablo(
            graph=self.graph,
            active_nodes=active_nodes)


    def select(self, filter):
        """
        Filters a graph by a function.

        Parameters:
            filter: Callable
                node attribute name to filter on

        Returns: 
            A new Graph instance
        """
        active_nodes = [x for x,y in self.graph.nodes(data=True) if filter(y)]
        return Diablo(
            graph=self.graph,
            active_nodes=active_nodes)


    def active_nodes(self, data=False):
        if not data:
            return self._active_nodes
        return [self.graph[node] for node in self._active_nodes]


    def list_relationships(self):
        relationships = []
        for node in self._active_nodes:
            relationships += {r for (s, t, r) in self.graph.outgoing_edges(node)}
        return set(relationships)
        

    def __repr__(self):
        return F"Graph - {len(list(self.graph.nodes()))} nodes ({len(self._active_nodes)} selected), {len(list(self.graph.edges()))} edges"

