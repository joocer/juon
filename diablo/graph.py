"""
Simplified graph data structure, only suitable for directed graphs.

- Edges are stored in a dictionary, the key is the source node
- Nodes are stored in a B+Tree

The structure is optimized for 
Traversing the graph is 
Getting the details of a specific node is fast

This is not a complete replacement for NetworkX, it is designed and
optimized for few use cases.

If you want to do more, translate to NetworkX.
"""

from .index import BPlusTree

BTREE_ORDER = 16

class Graph(object):

    __slots__ = ('_nodes', '_edges')

    def __init__(self):
        self._nodes = {}
        self._edges = {}


    def _make_a_list(self, obj):
        """ internal helper method """
        if isinstance(obj, list):
            return obj
        return [obj]


    def read_graphml(self, xml_file):
        import xmltodict
        # load the file into a dom
        with open(xml_file, 'r') as fd:
            xml_dom = xmltodict.parse(fd.read())

        # load the keys
        keys = {}
        for key in xml_dom['graphml'].get('key', {}):
            keys[key['@id']] = key['@attr.name']

        self._nodes = BPlusTree(BTREE_ORDER)
        # load the nodes
        for node in xml_dom['graphml']['graph'].get('node', {}):
            data = {}
            skip = False
            for key in self._make_a_list(node.get('data', {})):
                try:
                    data[keys[key['@key']]] = key.get('#text', '')
                except:
                    skip = True
            if not skip:
                self._nodes.insert(node['@id'], data)

        self._edges = {}
        for edge in xml_dom['graphml']['graph'].get('edge', {}):
            data = {}
            source = edge['@source']
            target = edge['@target']
            for key in self._make_a_list(edge.get('data', {})):
                data[keys[key['@key']]] = key['#text']
            if source not in self._edges:
                self._edges[source] = []
            self._edges[source].append((target, data))

#    def load(self, json_file):
#        import ujson as json
#        reader = inner_file_reader(json_file)
#        for row in reader:
#            record = json.loads(row)
#            if record['type'] == 'node':
#                self._nodes[record['id']] = record['attributes']
#            if record['type'] == 'edge':
#                self._edges[(record['source'], record['target'])] = record['attributes']

    def save(self, graph_path):
        import ujson as json

        self._edges.save(graph_path + '/edges.index')
        self._nodes.save(graph_path + '/nodes.index')
        
    def add_edge(self, source, target, **kwargs):
        # add the edge to the grapg
        self._edges.insert(source, (target, kwargs))

    def add_node(self, node_id, **kwargs):
        self._nodes[node_id] = kwargs

    def nodes(self, data=False):
        if data:
            return self._nodes.items()
        return self._nodes.keys()

    def edges(self):
        return self._edges.items()

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
        return {a for a,b in targets}

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


    def to_networkx(self):
        import networkx as nx
        raise NotImplementedError()

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


 
def inner_file_reader(
        file_name: str,
        chunk_size: int = 64*1024*1024,
        delimiter: str = "\n"):
    """
    This is the guts of the reader - it opens a file and reads through it
    chunk by chunk. This allows huge files to be processed as only a chunk
    at a time is in memory.
    """
    with open(file_name, 'r', encoding="utf8") as f:
        carry_forward = ""
        chunk = "INITIALIZED"
        while len(chunk) > 0:
            chunk = f.read(chunk_size)
            augmented_chunk = carry_forward + chunk
            lines = augmented_chunk.split(delimiter)
            carry_forward = lines.pop()
            yield from lines
        if carry_forward:
            yield carry_forward




def get_size(obj, seen=None):
    import sys
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__slots__'):
        size += sum([get_size(getattr(obj, k), seen) for k in obj.__slots__])
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size
