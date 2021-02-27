import xmltodict
from .index import BPlusTree

BTREE_ORDER = 16

class Graph(object):

    __slots__ = ('_nodes', '_edges')

    def __init__(self):
        self._nodes = {}
        self._edges = BPlusTree(BTREE_ORDER)


    def _make_a_list(self, obj):
        if isinstance(obj, list):
            return obj
        return [obj]


    def load_graphml(self, xml_file):
        # load the file into a dom
        with open(xml_file, 'r') as fd:
            xml_dom = xmltodict.parse(fd.read())

        # load the keys
        keys = {}
        for key in xml_dom['graphml'].get('key', {}):
            keys[key['@id']] = key['@attr.name']

        # load the nodes
        index = -1
        for index, node in enumerate(xml_dom['graphml']['graph'].get('node', {})):
            data = {}
            skip = False
            for key in self._make_a_list(node.get('data', {})):
                try:
                    data[keys[key['@key']]] = key.get('#text', '')
                except:
                    skip = True
            if not skip:
                self._nodes[node.get('@id')] = data

        # load the edges
        self._edges = BPlusTree(BTREE_ORDER)
        index = -1
        for index, edge in enumerate(xml_dom['graphml']['graph'].get('edge', {})):
            data = {}
            source = edge['@source']
            target = edge['@target']
            for key in self._make_a_list(edge.get('data', {})):
                data[keys[key['@key']]] = key['#text']
            self._edges.insert(source, (target, data))


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

        node_types = {}
        for node_id, attribs in self.nodes(data=True):
            node_types[attribs.get('node_type')] = 1

        for node_type in node_types:
            with open(graph_path + F'/node-{node_type}.jsonl', 'w') as json_file:
                for node_id, attribs in self.nodes(data=True):
                    if attribs.get('node_type') == node_type:
                        record = {'id':node_id,'attributes':attribs}
                        json_file.write(json.dumps(record) + '\n')



        


    def add_edge(self, source, target, **kwargs):
        # add the edge to the grapg
        self._edges.insert(source, (target, kwargs))


    def add_node(self, node_id, **kwargs):
        self._nodes[node_id] = kwargs


    def nodes(self, data=False):
        if data:
            return self._nodes.items()
        return list(self._nodes.keys())

    def edges(self, data=False):
        yield from self._edges.items(data=data)

    def out_going_edges(self, source):
        return self._edges.retrieve(source) or []

    def bfs(self, node, depth):
        if depth == 0:
            return []

        edges = self.out_going_edges(node)
        result = [node]
        if edges:
            for walked_edge in edges:
                result.append(walked_edge[0])
                result += self.bfs(walked_edge[0], depth - 1)

        return list(set(result))

    def copy(self):
        g = Graph()
        g._nodes = self._nodes.copy()
        g._edges = self._edges
        return g


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



if __name__ == "__main__":

    from pprint import pprint

    g = Graph()
    #g.add_node('abc', variable=123)
    #g.add_edge('a', 'b', variable=456)
    #g.add_node('a', variable=789)
#    load_graph_ml(r'graph/mitre-data.graphml')

    g.load_graphml('graph/mitre-data.graphml')

    for nid, node in g.nodes(data=True):
        node['node_type'] = node.get('kind')
        del node['kind']

    import time

    s = time.time_ns()
    for i in range(1000):
        out_going = g.out_going_edges('CWE-15')
    print((time.time_ns() - s) / 1e9, out_going)

    

    n = time.time_ns()
    for i in range(1000):
        out_going = [t for s,t in g.edges(data=True) if s == 'CWE-15']
    print((time.time_ns() - n) / 1e9, out_going)

    #pprint(g._nodes)
    #pprint(g._edges)

    #print(g._nodes)

    #g.save('graph/mitre')

    #g.edge_index.show()