# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2013-11-05 08:58
# modified : 2013-11-05 08:58
"""
Compute link communities from the data.
"""

__author__="Johann-Mattis List"
__date__="2013-11-05"

import networkx as nx
from clics_lib.gml2json import graph2json
import lingpy.thirdparty.linkcomm as lc
import os
os.system('rm lcommunities/*.json')

# load the graph
graph= nx.read_gml('output/clics.gml')

print("[i] loaded graph")

# get set of nodes
nodes = sorted(graph.nodes())

# create adjacency, edges, and weights (needed for link clustering)
adjacency = dict([(n,set()) for n in nodes])
edges = set()
weights = {}

# pnodes stores processed nodes (need to keep track of unconnected nodes)
pnodes = set()

# iterate over nodes and fill in adjacency
for i,nA in enumerate(nodes):
    for j,nB in enumerate(nodes):
        if i < j:

            try:
                w = graph.edge[nA][nB]['weight']

            except:
                w = 0

            if w > 0:
                edges.add((nA,nB))
                edges.add((nB,nA))
                adjacency[nA].add(nB)
                adjacency[nB].add(nA)
                weights[nA,nB] = w
                pnodes.add(nA)
                pnodes.add(nB)

# create linkcomm object
hlc = lc.HLC(adjacency,edges)

print("[i] Instantiated link communities.")

# get communities
comms = hlc.single_linkage(threshold=0.08,w=weights)
edge2cid = comms[0]

print("[i] Computed link communities.")

# retrieve clusterings for the nodes
clusters = dict([(n,[]) for n in nodes])

# retrieve the data
clr2nodes = dict()
clr2edges = dict()

# count the links of 
for edge,idx in edge2cid.items():
    nodeA,nodeB = edge[0],edge[1]

    try:
        clr2edges[idx] += [edge]
    except KeyError:
        clr2edges[idx] = [edge]
    try:
        clr2nodes[idx] += [nodeA,nodeB]
    except KeyError:
        clr2nodes[idx] = [nodeA,nodeB]

for idx in clr2nodes:
    clr2nodes[idx] = sorted(set(clr2nodes[idx]))

# delete all clusters that appear as subsets of larger clusters
delis = []
for keyA in sorted(clr2nodes):
    for keyB in sorted(clr2nodes):
        if keyA != keyB:
            valsA = set(clr2nodes[keyA])
            valsB = set(clr2nodes[keyB])
            
            if valsA != valsB:
                if valsA.issubset(valsB):
                    delis += [keyA]
                elif valsB.issubset(valsA):
                    delis += [keyB]
            elif valsA == valsB:
                delis += [keyB]
for k in set(delis):
    del clr2nodes[k]

print("[i] cleaned link communities.")
# renumber the data
mapper = dict(zip(clr2nodes.keys(),range(1,len(clr2nodes)+1)))

comms = {}
found = []
for idx in clr2nodes:
    comms[mapper[idx]] = clr2nodes[idx]
    found += clr2nodes[idx]
missing = [f for f in nodes if f not in found]
idx = max(comms.keys())+1
for m in missing + [p for p in nodes if p not in pnodes]:
    comms[idx] = [m]
    idx += 1

def clean(s): return ''.join([x for x in s if x not in "/;?!.()[]"])

# retrieve community output from graph
f = open("output/lcommunitites.csv",'w')
for i,c in enumerate(comms):
    
    # get the subgraph
    subG = graph.subgraph(comms[c])

    n = sorted(subG.degree().items(),key=lambda x:x[1], reverse=True)[0][0]
    d = graph.node[n]['label']

    # copy components of graph to new graph
    newG = nx.Graph()

    for n,data in subG.nodes(data=True):

        newG.add_node(
                data['label'],
                key = data['key'],
                body_part = int(data['body_part']),
                swadesh100 = int(data['swadesh100'])
                )
    for nA,nB,data in subG.edges(data=True):
        newG.add_edge(
                subG.node[nA]['label'],
                subG.node[nB]['label'],
                **data
                )

    graph2json(newG,'lcommunities/cluster_{0}_{1}'.format(c,clean(d)))
    print("[i] Converting community number {0} / {1} ({2} nodes).".format(c,d,len(newG.nodes())))
    
    f.write('cluster_{0}_{1}.json'.format(c,d))
     
