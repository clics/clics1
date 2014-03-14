# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-03-11 12:46
# modified : 2014-03-11 12:46
"""
Convert the clusters produced by the community detection algorithms to sqlite.
"""

__author__="Johann-Mattis List"
__date__="2014-03-11"

import sqlite3 
from clics_lib.csv import *

nodes = csv2list('output/nodes2communities.csv')

conn = sqlite3.connect('website/clics.de/data/clips.sqlite3')
cursor = conn.cursor()
try:
    cursor.execute('drop table communities;')
except:
    pass

cursor.execute('create table communities(id,gloss,community,path,label,size);')

comms = [line[4] for line in nodes]
ccount = {}
for c in set(comms):
    ccount[c] = comms.count(c)

for node in nodes:
    cursor.execute(
            'insert into communities values(?,?,?,?,?,?);', 
            tuple(node+[ccount[node[-1]]])
            )
conn.commit()
