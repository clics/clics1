# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-02-17 13:52
# modified : 2014-02-17 13:52
"""
Normalize edge weights following Dellert's proposal.
"""

__author__="Johann-Mattis List"
__date__="2014-02-17"

import networkx as nx
import igraph as ig
from sys import argv
from lingpy import *

occs = dict(csv2list('output/foccurrences.txt', dtype=[str,int]))

gml = ig.read('output/clics.gml')

g = nx.Graph()

for edge in gml.es:
    source = gml.vs[edge.source]['concept']
    target = gml.vs[edge.target]['concept']
    weight = edge['weight']

    keyA = gml.vs[edge.source]['key']
    keyB = gml.vs[edge.target]['key']

    sizeA = gml.vs[edge.source]['frequency']
    sizeB = gml.vs[edge.target]['frequency']

    if source in g:
        pass
    else:
        g.add_node(source, **gml.vs[edge.source].attributes())

    if target in g:
        pass
    else:
        g.add_node(target, **gml.vs[edge.target].attributes())
    g.add_edge(source,target,**edge.attributes())


def normalize(freqA, freqB, weight):
    """
    Normalize edge weights following Dellert's proposal.
    """

    return weight ** 2 / (freqA + freqB - weight)

for nA, nB, data in list(g.edges(data=True)):

    w = data['families']
    fA = occs[g.node[nA]['key']]
    fB = occs[g.node[nB]['key']]

    nw = normalize(fA, fB, w)
    if nw > 0:
        data['normalized_weight'] = nw * 800
    else:
        g.remove_edge(nA, nB)

with open('output/clics_b.gml', 'w') as f:
    for line in nx.generate_gml(g):
        f.write(line+'\n')
#nx.write_gml(g, 'output/clics_b.gml')

