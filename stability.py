# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-03-11 17:03
# modified : 2014-03-11 17:03
"""
compute stability measures for clics
"""

__author__="Johann-Mattis List"
__date__="2014-03-11"

from lingpy import *
import networkx as nx
import pickle

try:
    g = pickle.load(open('bin/clics.bin', 'rb'))
except:
    g = nx.read_gml('output/clics_b.gml')
    pickle.dump(g,open('bin/clics.bin', 'wb'))


for n,d in g.nodes(data=True):
    if d['key'] == '1.42':
        idx = n
g.remove_node(idx)

asjp1 = csv2list('concepts_asjp.csv')
asjp = dict([(d[1],d[0]) for d in asjp1[1:]]) #dict(bas.get_sublist('asjp', 'ids', 'number', 'item'))


# get the degree 
deg = nx.degree(g,weight='normalized_weight')
deg2 = nx.degree(g,weight='families')
deg3 = nx.degree(g,weight='languages')

DEG = {}
for k in deg:
    DEG[g.node[k]['key']] = deg[k]

DEG2 = {}
for k in deg2:
    DEG2[g.node[k]['key']] = deg2[k]

DEG3 = {}
for k in deg3:
    DEG3[g.node[k]['key']] = deg3[k]



occs = dict(csv2list('output/occurrences.txt', dtype=[str,int]))

DEG4 = {}
for k in DEG3:
    DEG4[k] = DEG3[k] / occs[k]

f = open('degrees_asjp.csv', 'w')
f.write('Concept\tIDSKEY\tLanguages\tFamilies\tOccurrences\tLanguages/Occurrences\n')
for n,i in sorted(asjp.items(), key=lambda x:x[1]):
    f.write(i+'\t'+n+'\t'+'{0}\t{1}\t{2}\t{3:.2f}'.format(int(DEG3[n]),int(DEG2[n]),occs[n],
        DEG3[n] / occs[n])+'\n')
f.close()

f = open('degrees_full.csv', 'w')
lines = []
f.write('IDSKEY\tLABEL\tLanguages\tFamilies\tOccurrences\tLanguages/Occurrences\n')
for node,data in sorted(g.nodes(data=True), key= lambda x: DEG4[x[1]['key']]):
    if data['key'] in asjp:
        asjp_item = '*'
    else:
        asjp_item = ''
    f.write('{3}{0}\t{1}\t{2}\t{4}\t{5}\t{6:.2f}\n'.format(
        data['key'], data['label'], int(deg3[node]), asjp_item, int(deg2[node]),
        occs[data['key']], DEG4[data['key']]))
f.close()
