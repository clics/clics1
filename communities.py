# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2013-10-29 17:36
# modified : 2013-10-29 17:36
"""
Compute subsets of the graphs with help of community detection analyses.
"""

__author__="Johann-Mattis List"
__date__="2013-10-29"


import igraph as ig
import networkx as nx
from clics_lib.gml2json import graph2json
from sys import argv

# read the graph from gml
g = ig.read("clics.gml")

if len(argv) == 1:
    # analyze graph with infomap
    coms = g.community_edge_betweenness(directed=False,weights='weight')
    
    # get communities, currently we force algorithm to get us 100 communities for
    # convenience
    communities = coms.as_clustering(250)
elif 'infomap' in argv:
    communities = g.community_infomap(edge_weights='weight')

print('[i] Computed communities.')

# copy graph to networkx
newg = nx.Graph()

for edge in g.es:

    s,t = edge.source, edge.target

    if s not in newg:
        label = g.vs[s]['label']
        key = g.vs[s]['key']
        body_part = int(g.vs[s]['body_part'])
        swadesh100 = int(g.vs[s]['swadesh100'])

        newg.add_node(
                label,
                key=key,
                body_part=body_part,
                swadesh100=swadesh100
                )
    
    if t not in newg:
        label = g.vs[t]['label']
        key = g.vs[t]['key']
        body_part = int(g.vs[t]['body_part'])
        swadesh100 = int(g.vs[t]['swadesh100'])

        newg.add_node(
                label,
                key=key,
                body_part=body_part,
                swadesh100=swadesh100
                )

    
    # get labels again for consistency
    labelS = g.vs[s]['label']
    labelT = g.vs[t]['label']

    try:
        newg[s][t]
    except KeyError:
        newg.add_edge(
                labelS,
                labelT,
                weight = edge['weight'],
                languages = edge['languages'],
                families = edge['families']
                )


comms = []
for i,s in enumerate(communities.subgraphs()):

    for node in s.vs:
        idx = node['label']
        newg.node[idx]['community'] = i+1

    comms += [i+1]



nx.write_gml(newg,'clics_communities.gml')

# get nodes with communities
nodes = [n for n in newg.nodes(data=True) if 'community' in n[1]]

# write all communities to separate json-graphs
for c in comms:
    
    subG = newg.subgraph(
            [n[0] for n in nodes if n[1]['community'] == c]
            )
    # get node with highest degree
    d = sorted(subG.degree().items(),key=lambda x:x[1],reverse=True)[0][0]

    graph2json(subG,'communities/cluster_{0}_{1}'.format(c,d))
    print("[i] Converting community number {0} / {1} ({2} nodes).".format(c,d,len(subG.nodes()))
            )



