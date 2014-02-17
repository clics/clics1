# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-02-17 14:17
# modified : 2014-02-17 14:17
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2014-02-17"


import networkx as nx
from clics_lib.csv import *
from clics_lib.gml2json import *

# load the data
data = csv2list('output/links.sqlite3.txt')

# load swadesh metadata
swa100 = csv2list('data/swa100.txt')

swaDict = {}
for line in swa100:
    if '--' in line[1]:
        k3 = None
        try:
            k1,k2 = line[1].split(' -- ')
        except:
            k1,k2,k3 = line[1].split(' -- ')
        
        if k3:
            swaDict[k2] = (k1,line[0])
            swaDict[k3] = (k1,line[0])
        else:
            swaDict[k2] = (k1,line[0])
    else:
        swaDict[line[1]] = (line[1],line[0])

keyocc = dict([(a,b) for a,b in csv2list('output/occurrences.txt')])

# load the graph
g = nx.Graph()

for line in data:
    keyA,keyB = line[2],line[3]
    concA,concB = line[0],line[1]
    linksF,linksL = line[4],line[5]
    
    try:
        g.node[keyA]
    except:
        if keyA.startswith('4'):
            if int(keyA[2]) in [1,2,3,4]:
                bp = 1
            else:
                bp = 0
        else:
            bp = 0

        if concA in swaDict:
            swadesh = True
        else:
            swadesh = False

        g.add_node(
                keyA,
                concept=concA,
                key = keyA,
                label = concA,
                body_part = bp,
                swadesh100 = swadesh,
                frequency = int(keyocc[keyA])
                )

    try:
        g.node[keyB]
    except:
        if keyB.startswith('4'):
            if int(keyB[2]) in [1,2,3,4]:
                bp = 1
            else:
                bp = 0
        else:
            bp = 0
        
        if concB in swaDict:
            swadesh = True
        else:
            swadesh = False

        g.add_node(
                keyB,
                concept=concB,
                label = concB,
                key = keyB,
                body_part = bp,
                swadesh100 = swadesh,
                frequency = int(keyocc[keyB])
                )

    g.add_edge(
            keyA,
            keyB,
            weight = int(linksF),
            families = int(linksF),
            languages = int(linksL)
            )

nx.write_gml(g,'output/clics.gml')

graph2json(g,'output/clics')
          
