# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-03-13 12:31
# modified : 2014-03-13 12:31
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2014-03-13"

from clics_lib.csv import *
import json

links = csv2list('output/links.sqlite3.txt')

words = []
for link in links:
    keyA,keyB = link[0],link[1]
    forms = link[6].split('//')
    for i,f in enumerate(forms):
        lng = f[:f.index(':')]
        wrd = f[f.index(':')+2:-1]
        forms[i] = lng+':'+wrd.replace(':', 'ː')
    words += [dict(
            words = forms,
            key = keyA+'___'+keyB
            )]

with open('website/clics.de/data/words.json', 'w') as f:
    f.write(json.dumps(words))

