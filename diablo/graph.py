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

from .index.btree import BTree


BTREE_ORDER = 16

class Graph(object):

    __slots__ = ('_nodes', '_edges')

    def __init__(
            self,
            graph = None):

        if graph is None:
            self._nodes = BTree(BTREE_ORDER)
            self._edges = {}
        else:
            self._nodes = graph._nodes
            self._edges = graph._edges
    

    def _make_a_list(self, obj):
        """ internal helper method """
        if isinstance(obj, list):
            return obj
        return [obj]


    def save(self, graph_path):
        import ujson as json
        with open(graph_path + '/edges.jsonl', 'w') as edge_file:
            for source, target, relationship in self.edges():
                edge_record = {"source": source, "target": target, "relationship": relationship}
                edge_file.write(json.dumps(edge_record) + '\n')
        self._nodes.save(graph_path + '/nodes.jsonl')

        
    def add_edge(self, source, target, relationship):
        # add the edge to the graph
        if source not in self._edges:
            targets = []
        else:
            targets = self._edges[source]
        targets.append((target, relationship,))
        self._edges[source] = list(set(targets))


    def add_node(self, node_id, **kwargs):
        self._nodes.insert(node_id, kwargs)


    def nodes(self, data=False):
        if data:
            return self._nodes.items()
        return self._nodes.keys()


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
        queue = deque([(source, self.outgoing_edges(source))])
        
        while queue:
            parent, children = queue[0]
            try:
                child = children.pop()
                if child not in visited:
                    yield parent, child
                    visited.add(child)
                    queue.append((child, self.outgoing_edges(child)))
            except KeyError:
                queue.popleft()


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
        import networkx as nx  # type:ignore
        g = nx.DiGraph()
        for s, t, r in graph.edges():
            g.add_edge(s, t, relationship=r)
        for node, attribs in graph.nodes(True):
            if 'kind' in attribs:
                attribs['node_type'] = attribs['kind']
                del attribs['kind']
            g.add_node(node, **attribs)
        return g

    def epitomize(graph):
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
        node = self._nodes.retrieve(nid)
        if len(node) > 0:
            return node[0]
        return {}


