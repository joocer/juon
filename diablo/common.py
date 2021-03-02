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
from .graph import Graph
from .index import Index
try:
    import xmltodict  # type:ignore
except ImportError:
    pass

BTREE_ORDER = 16

def load_graphml(
        xml_file: str):
    """

    Parameters:
        xml_file: string
    """
    with open(xml_file, 'r') as fd:
        xml_dom = xmltodict.parse(fd.read())

    g = Graph()

    # load the keys
    keys = {}
    for key in xml_dom['graphml'].get('key', {}):
        keys[key['@id']] = key['@attr.name']

    g._nodes = Index(BTREE_ORDER)
    # load the nodes
    for node in xml_dom['graphml']['graph'].get('node', {}):
        data = {}
        skip = False
        for key in g._make_a_list(node.get('data', {})):
            try:
                data[keys[key['@key']]] = key.get('#text', '')
            except:
                skip = True
        if not skip:
            g._nodes.insert(node['@id'], data)

    g._edges = {}
    for edge in xml_dom['graphml']['graph'].get('edge', {}):
        data = {}
        source = edge['@source']
        target = edge['@target']
        for key in g._make_a_list(edge.get('data', {})):
            data[keys[key['@key']]] = key['#text']
        if source not in g._edges:
            g._edges[source] = []
        g._edges[source].append((target, data))

    return g

# def load(self, json_file):
#        import ujson as json
#        reader = inner_file_reader(json_file)
#        for row in reader:
#            record = json.loads(row)
#            if record['type'] == 'node':
#                self._nodes[record['id']] = record['attributes']
#            if record['type'] == 'edge':
#                self._edges[(record['source'], record['target'])] = record['attributes']
