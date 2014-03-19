# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-02-07 14:37
# modified : 2014-02-07 14:37
"""
Load the networkx-graph and retrieve a specific cluster.
"""

__author__="Johann-Mattis List"
__date__="2014-02-07"

from clics_lib.csv import *
import networkx as nx
import igraph as ig
from sys import argv

gml = ig.read('output/clics_c.gml')
comms = dict([(k[0],k[3]) for k in csv2list('output/nodes2communities.csv')])
g = nx.Graph()



for edge in gml.es:
    source = gml.vs[edge.source]['concept']
    target = gml.vs[edge.target]['concept']
    weight = edge['weight']
    if source not in g:
        tmp = gml.vs[edge.source].attributes()
        tmp['out_edge'] = []
        del tmp['id']
        g.add_node(source,**tmp)
    if target not in g:
        tmp = gml.vs[edge.target].attributes()
        del tmp['id']
        tmp['out_edge'] = []
        g.add_node(target,**tmp)

    g.add_edge(source,target,**edge.attributes())

if argv[1] == 'ALL':
    nodes = [n for n in g.nodes() if n.strip()]
else:
    nodes = [argv[1]]

dset = {}

os.system('git rm website/clics.de/data/cuts/*.json')
os.system('rm website/clics.de/data/cuts/*.json')

nodeD = dict()
blacklist = []
for this_node in nodes:
    if this_node not in blacklist:
        
        direct_neighbor = []

        subg = nx.Graph()
        queue = [(this_node, g.edge[this_node],0)]
        
        weight = 4
        weightB = 4
        
        while queue:
            
            source,neighbors,generation = queue.pop(0)
            for n,d in neighbors.items():
                if n.strip():
                    if d['families'] > weight:
                        subg.add_node(n,**g.node[n])
                        subg.add_edge(source,n,**d)
                        queue += [(n,g.edge[n],generation+1)]
                    elif d['families'] > weightB:
                        subg.add_node(n,**g.node[n])
                        subg.add_edge(source,n,**d)
                    
                    # check for common nodes
                    #if generation == 0 and d['families'] > weightB:
                    #    if n in dset:
                    #        direct_neighbor = n
            
            if generation > 2:
                break
        
        # repeat if no good results are found
        if len(subg) < 5:
            weight = 3
            weightB = 3

        subg = nx.Graph()
        queue = [(this_node, g.edge[this_node],0)]
        
        
        while queue:
            
            source,neighbors,generation = queue.pop(0)
            for n,d in neighbors.items():
                if n.strip():
                    if d['families'] > weight:
                        subg.add_node(n,**g.node[n])
                        subg.add_edge(source,n,**d)
                        queue += [(n,g.edge[n],generation+1)]
                    elif d['families'] > weightB:
                        subg.add_node(n,**g.node[n])
                        subg.add_edge(source,n,**d)
                    
                    # check for common nodes
                    #if generation == 0 and d['families'] > weightB:
                    #    if n in dset:
                    #        direct_neighbor = n
            
            if generation > 2:
                break

        for n,d in subg.nodes(data=True):
            links = g.edge[n]
            for l in links:
                if l not in subg:
                    if g.edge[n][l]['families'] > weightB:
                        if 'out_edge' not in d:
                            d['out_edge'] = []
                            
                        d['out_edge'] += [
                                (
                                    comms[g.node[l]['key']],
                                    l,
                                    g.edge[n][l]['families'],
                                    g.edge[n][l]['weight'],
                                    'x'
                                    )
                                ]
                        d['out_edge'] = sorted(set(d['out_edge']), key=lambda
                                x:x[2])
        
        from clics_lib.gml2json import *

        if '/' in this_node:
            nodename = this_node.replace('/','_')
        else:
            nodename = this_node
        
        
        nodeD[this_node] = [n for n in subg.nodes() if n.strip()]
        dset[this_node] = [g.node[this_node]['key'], len(nodeD[this_node]), 'network_'+nodename+'_'+str(len(nodeD[this_node]))]

labels = {}
for n in nodeD:

    subg = g.subgraph(nodeD[n]+[n])

    label = sorted(subg.degree().items(),key=lambda x:x[1],reverse=True)[0][0] 
    labels[n] = label
    
    for node,data in subg.nodes(data=True):
        dels = []
        data['out_edge'] = sorted(set([tuple(t) for t in data['out_edge']]), key=lambda x:x[2],
                reverse=True)
        for i,(a,b,c,d,e) in enumerate(data['out_edge']):
            if b in nodeD[n]+[n]:
                #pass
                dels += [i]
            else:
                clabel = a.split('_')[-1]
                print(clabel,a)
                try:
                    data['out_edge'][i] = [a,b,c,d,clabel]
                    print(n)
                except:
                    dels += [i]

        for i in dels[::-1]:
            del data['out_edge'][i]

    #for node,data in subg.nodes(data=True):
    #    for i,(a,b,c,d,e) in enumerate(data['out_edge']):
    #        data[i] = [a,b,c,d,e.split('_')[-1]]
    
    if '/' in n:
        nodename = n.replace('/','_')
    else:
        nodename = n

    if len(subg) > 1:
        graph2json(subg,'website/clics.de/data/cuts/network_'+nodename+'_'+str(len(subg.nodes())))
    print(len(subg))
    
with open('output/nodes2cuts.csv', 'w') as f:
    for key in dset:
        line = [key] + [k for k in dset[key]]
        f.write('\t'.join([str(x) for x in line])+'\n')

#os.system('git add cuts/*.json')

maxvals = []
import sqlite3

conn = sqlite3.connect('website/clics.de/data/clips.sqlite3')
cursor = conn.cursor()
try:
    cursor.execute('drop table cuts;')
except:
    pass

cursor.execute('create table cuts(id,gloss,path,size,label);')

for a in dset:
    b,c,d = dset[a]
    if a.strip():
        cursor.execute(
                'insert into cuts values(?,?,?,?,?);', 
                (b,a,d,c,labels[a])
                )
        maxvals += [c]
conn.commit()
print(max(maxvals))

os.system('git add website/clics.de/data/cuts/*.json')

