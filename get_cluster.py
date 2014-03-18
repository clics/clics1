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
    nodes = g.nodes()
else:
    nodes = [argv[1]]

dset = {}

os.system('git rm cuts/*.json')
os.system('rm cuts/*.json')

blacklist = []
for this_node in nodes:
    if this_node not in blacklist:
        
        direct_neighbor = False

        subg = nx.Graph()
        queue = [(this_node, g.edge[this_node],0)]
        
        weight = 5
        weightB = 2
        
        while queue:
            
            source,neighbors,generation = queue.pop(0)
            for n,d in neighbors.items():
                if d['families'] > weight:
                    subg.add_node(n,**g.node[n])
                    subg.add_edge(source,n,**d)
                    queue += [(n,g.edge[n],generation+1)]
                elif d['families'] > weightB:
                    subg.add_node(n,**g.node[n])
                    subg.add_edge(source,n,**d)
                
                # check for common nodes
                if generation == 0 and d['families'] > weightB:
                    if n in dset:
                        direct_neighbor = n

        
            if generation > 2:
                break
        
        for n,d in subg.nodes(data=True):
            links = g.edge[n]
            for l in links:
                if l not in subg:
                    if g.edge[n][l]['families'] > weight:
                        d['out_edge'] += [
                                (
                                    comms[g.node[l]['key']],
                                    l,
                                    g.edge[n][l]['families'],
                                    g.edge[n][l]['weight']
                                    )
                                ]
        
        from clics_lib.gml2json import *

        if '/' in this_node:
            nodename = this_node.replace('/','_')
        else:
            nodename = this_node
        

        if len(subg) > 5 and not direct_neighbor:

            graph2json(subg,'cuts/network_'+nodename+'_'+str(len(subg.nodes())))
            print(len(subg))
            dset[this_node] = [g.node[this_node]['key'],len(subg),
                'network_'+nodename+'_'+str(len(subg))]
        elif direct_neighbor:
            dset[this_node] = [g.node[this_node]['key'], dset[direct_neighbor][1],
                    dset[direct_neighbor][2]]
    
with open('output/nodes2cuts.csv', 'w') as f:
    for key in dset:
        line = [key] + [k for k in dset[key]]
        f.write('\t'.join([str(x) for x in line])+'\n')

os.system('git add cuts/*.json')


import sqlite3

conn = sqlite3.connect('website/clics.de/data/clips.sqlite3')
cursor = conn.cursor()
try:
    cursor.execute('drop table cuts;')
except:
    pass

cursor.execute('create table cuts(id,gloss,path,size);')

for a in dset:
    b,c,d = dset[a]
    if a.strip():
        cursor.execute(
                'insert into cuts values(?,?,?,?);', 
                (b,a,c,d)
                )
conn.commit()
