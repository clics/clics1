# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2013-07-12 14:36
# modified : 2013-08-30 14:32
"""
script calculates basic statistics on the languages in the sample
"""

__author__="Johann-Mattis List"
__date__="2013-08-30"


from glob import glob
from re import sub
from clics_lib.csv import *

globs = glob('wordlists/*.csv')

blacklist = ["lat","epo"]

data = []
for f in globs:
    print(f)
    tmpB = {}
    for line in open(f):
        if line.startswith('@'):
            a,b = line.split(':')
            tmpB[a[1:].strip()] = b.strip()
        else:
            pass

    # get the data
    cls = tmpB['classification']
    fam = tmpB['classification'].split(',')[0]
    iso = tmpB['iso']
    siz = tmpB['size']
    src = tmpB['source']
    var = tmpB['variety']
    nam = tmpB['language']

    # check for wrong stuff
    if cls == "<not yet checked>" or iso in blacklist:
        pass
    else:
        # append stuff to data
        data += [[nam,iso,var,fam,siz,src,cls]]

out = open('output/clics.stats','w')
out.write(
        "\t".join([
            "LANGUAGE",
            "ISO",
            "VARIETY",
            "FAMILY",
            "SIZE",
            "SOURCE",
            "CLASSIFICATION"
            ])+'\n')

wordnum = 0
fams = []
for line in sorted(data,key=lambda x:(x[3],int(x[4]),x[0])):
    out.write('\t'.join(line)+'\n')
    wordnum += int(line[4])
    fams += [line[3]]
out.close()

print("Number of languages in sample {0}".format(len(data)))
print("Number of words in sample {0}".format(wordnum))
print("Number of words in sample {0}".format(len(set(fams))))
