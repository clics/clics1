# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-02-07 14:37
# modified : 2014-02-07 14:37
"""
Load the networkx-graph and retrieve a specific cluster.
"""

__author__="Johann-Mattis List"
__date__="2014-02-07"

import networkx as nx
import igraph as ig
from sys import argv

gml = ig.read('output/clics_b.gml')

g = nx.Graph()

for edge in gml.es:
    source = gml.vs[edge.source]['concept']
    target = gml.vs[edge.target]['concept']
    weight = edge['weight']
    g.add_edge(source,target,**edge.attributes())

subg = nx.Graph()
queue = [(argv[1], g.edge[argv[1]],0)]

while queue:
    
    source,neighbors,generation = queue.pop(0)

    for n,d in neighbors.items():
        if d['weight'] > 3:
            subg.add_edge(source,n,**d)
            queue += [(n,g.edge[n],generation+1)]
        elif d['weight'] > 2:
            subg.add_edge(source,n,**d)

    if generation > 2:
        break

nx.write_gml(subg, 'output/'+argv[1]+str(len(subg.nodes()))+'.gml')

from clics_lib.gml2json import *
gml2json('output/'+argv[1]+str(len(subg.nodes()))+'.gml')


