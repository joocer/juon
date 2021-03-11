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

import orjson as json

class Graph(object):
    """
    Graph object, optimized for traversal.

    Edges are stored in a dictionary, the key is the source node to speed up 
    finding outgoing edges. The Edges only have three pieces of data:
        - the source node (the key)
        - the target node
        - the relationship
    The target and the relationship are stored as a tuple, the edge dictionary
    stores lists of tuples.

    Nodes are stored as a B+Tree, this gives slightly slower performance 
    than a dictionary but has a distinct advantage in that it sorts the
    values enabling binary searching of the dataset without loading into
    memory.
    """
    __slots__ = ('_nodes', '_edges')

    def __init__(self):
        """
        Directed Graph.
        """
        self._nodes = {}
        self._edges = {}
    

    def _make_a_list(self, obj):
        """ internal helper method """
        if isinstance(obj, list):
            return obj
        return [obj]


    def save(self, graph_path):
        """
        Persist a graph to storage. It saves nodes and edges to separate files.

        Parameters:
            graph_path: string
                The folder to save the node and edge files to
        """
        
        #with open(graph_path + '/edges.jsonl', 'w') as edge_file:
        #    for source, target, relationship in self.edges():
        #        edge_record = {"source": source, "target": target, "relationship": relationship}
        #        edge_file.write(json.dumps(edge_record) + '\n')
        with open(graph_path + '/nodes.jsonl', 'w') as node_file:
            for nid, attributes in self.nodes(data=True):
                node_record = {"nid": nid, "attributes": attributes}
                node_file.write(json.dumps(node_record) + '\n')


    def add_edge(self, source, target, relationship):
        """
        Add edge to the graph
        """
        if source not in self._edges:
            targets = []
        else:
            targets = self._edges[source]
        targets.append((target, relationship,))
        self._edges[source] = list(set(targets))


    def add_node(self, nid, **kwargs):
        self._nodes[nid] = kwargs


    def nodes(self, data=False):
        if data:
            return self._nodes.items()
        return list(self._nodes.keys())


    def edges(self):
        for s, records in self._edges.items():
            for t, r in records:
                yield s, t, r


    def breadth_first_search(
            self,
            source):
        """
        Search a tree for nodes we can walk to from a given node. This uses a 
        variation of the algorith used by NetworkX optimized for the Diablo
        data structures.
        
        https://networkx.org/documentation/networkx-1.10/_modules/networkx/algorithms/traversal/breadth_first_search.html#bfs_tree
        
        Parameters:
            source: string
                The node to walk from
        """
        from collections import deque
        
        visited = set([source])
        queue = deque([self.outgoing_edges(source)])

        new_edges = {}
        
        while queue:
            children = queue[0]
            try:
                child = children.pop()
                if child not in visited:

                    s,t,r = child
                    targets = new_edges.get(source, [])
                    targets.append((t, r,))
                    new_edges[s] = targets

                    visited.add(child)
                    queue.append((child, self.outgoing_edges(child)))
            except KeyError:
                queue.popleft()

        return new_edges

    def outgoing_edges(
            self,
            source):
        targets = self._edges.get(source) or {}
        return {(source, t, r) for t, r in targets}


    def descendants_at_distance(
            self,
            source,
            distance):

        current_distance = 0
        queue = {source}
        visited = {source}

        while queue:
            if current_distance == distance:
                return queue
            current_distance += 1
            next_vertices = set()
            for vertex in queue:
                for child in self.outgoing_edges(vertex):
                    if child not in visited:
                        visited.add(child)
                        next_vertices.add(child)
            queue = next_vertices
        return set()


    def copy(self):
        g = Graph()
        g._nodes = self._nodes.copy()
        g._edges = self._edges.copy()
        return g


    def subgraph(self, node_list):
        # create a graph based on the nodes we have been given
        new_graph = Graph()
        for node in node_list:
            edges = self._edges[node]
            for target, attrib in edges:
                if target in node_list:
                    new_graph.add_edge(node, target, **attrib)
            new_graph.add_node(node, self._nodes[node])
        return new_graph


    def to_networkx(graph):
        """
        Convert a Diablo graph to a NetworkX graph
        """
        import networkx as nx  # type:ignore
        g = nx.DiGraph()
        for s, t, r in graph.edges():
            g.add_edge(s, t, relationship=r)
        for node, attribs in graph.nodes(True):
            g.add_node(node, **attribs)
        return g

    def epitomize(graph):
        """
        Summarize a Graph by reducing to only the node_types and relationships
        """
        g = Graph()
        for s, t, r in graph.edges():
            node1 = graph[s]
            node2 = graph[t]
            if node1 and node2:
                g.add_edge(node1.get('node_type'), node2.get('node_type'), r)
            if node1:
                g.add_node(node1.get('node_type'), node_type=node1.get('node_type'))
            if node2:
                g.add_node(node2.get('node_type'), node_type=node2.get('node_type'))
        return g


    def __repr__(self):
        return F"Graph - {len(list(self.nodes()))} nodes, {len(list(self.edges()))} edges"

    def __len__(self):
        return len(list(self.nodes()))

    def __getitem__(self, nid):
        return self._nodes.get(nid, {})


