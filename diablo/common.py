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
import types
from .graph import Graph
from .diablo import Diablo
from .index.btree import BTree
from .errors import NodeNotFoundError
try:
    import xmltodict  # type:ignore
except ImportError:
    pass

BTREE_ORDER = 16

def _make_a_list(obj):
    """ internal helper method """
    if isinstance(obj, (list, types.GeneratorType)):
        return obj
    return [obj]


def walk(graph, nids):
    """
    Begin a traversal by selecting the matching nodes.

    Parameters:
        *nids: strings
            the identity(s) of the node(s) to select

    Returns:
        A Diablo instance
    """
    nids = _make_a_list(nids)
    if len(nids) > 0:
        active_nodes = [nid for nid in graph.nodes() if nid in nids]
        if len(active_nodes) == 0:
            raise NodeNotFoundError("No matching nodes found")
        return Diablo(
            graph=graph,
            active_nodes=active_nodes)
    else:
        return Diablo(graph, set())


def read_graphml(
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

    g._nodes = BTree(BTREE_ORDER)
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
        g.add_edge(source, target, data.get('relationship'))

    return g

def load(path):

    import ujson as json

    g = Graph()
    g._nodes = BTree.read_file(path + '/nodes.jsonl')

    with open(path + '/edges.jsonl', 'r') as edge_file:
        for line in edge_file:
            edge = json.loads(line)
            g.add_edge(edge['source'], edge['target'], edge['relationship'])

    return g