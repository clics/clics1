# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2013-08-30 14:59
# modified : 2013-08-30 14:59
"""
Calculate the links from wordlist data.
"""

__author__="Johann-Mattis List"
__date__="2013-08-30"


from glob import glob
from sys import argv
import sys
import re
import sqlite3
import os
from clics_lib.csv import *

if len(argv) == 1 or "-h" in argv or "--help" in argv:
    print("Usage: python[3] links.py FOLDER")
    sys.exit()
else:
    pass


# get the converters for the sources of ids and wold
ids_sources = dict(csv2list('data/ids_meta_data.txt'))

# get the wold-sources
wold_sources = dict(csv2list('data/wold_meta_data.txt'))

if not argv[1].endswith('/'):
    files = glob(argv[1]+'/*.csv')
else:
    files = glob(argv[1]+'*.csv')

# ids and wold  website as avriable
ids_web="http://lingweb.eva.mpg.de/cgi-bin/ids/ids.pl?com=simple_browse&lg_id={0}"
wold_web="http://wold.livingsources.org/vocabulary/{0}"

links = {}

blacklist = [
        "lat",
        "epo",
        ]

invalid = []

for f in files:
    print("[i] Processing file {0}...".format(f))
    infile = open(f)
    data = []
    tags = {}
    for line in infile:
        # get the data
        if not line.startswith('@'):
            data.append(line.strip().split('\t'))
        # get the tags
        else:
            key,value = re.findall(r'@(.+): (.+)\n',line)[0]
            tags[key] = value
        tags['id'] = f.split('/')[-1].split('-')[-1].replace('.csv','')
        try:
            variety = tags['id'].split('_')[1]
        except:
            variety = 'standard'
        tags['variety'] = variety

    # discard languages that are not contemporary
    if tags['classification'] == "<not yet checked>" or tags['iso'] in blacklist:
        print("[!] File {0} is not valid.".format(f))
        invalid += [f]
    else:
        # get all identical data by looping over all data
        for i,(numberA,glossA,wordA) in enumerate(data):
            for j,(numberB,glossB,wordB) in enumerate(data):
                if i < j:
                    # modify words, replace damn "'" by some other symbol
                    wordA = wordA.replace("'", "ˈ")
                    wordB = wordB.replace("'","ˈ")
                    if wordA == wordB:
                        if (numberA,numberB) in links:
                            links[numberA,numberB]['occurrences'] += 1
                            links[numberA,numberB]['evidence'] += [
                                    (
                                        sorted(tags.items()),
                                        wordA
                                        )]
                            links[numberB,numberA] = links[numberA,numberB]
                        elif (numberB,numberA) in links:
                            links[numberB,numberA]['occurrences'] += 1
                            links[numberB,numberA]['evidence'] += [
                                    (
                                        sorted(tags.items()),
                                        wordA
                                        )]
                            links[numberA,numberB] = links[numberB,numberA]

                        else:
                            links[numberA,numberB] = {
                                    'occurrences':1,
                                    'evidence':[(sorted(tags.items()),wordA)] }
                            links[numberB,numberA] = links[numberA,numberB]


# get ids-keys
ids_keys = {}
infile = open('data/ids_keys')
for line in infile:
    key,value = line.strip().split('\t')
    ids_keys[key] = value


# start writing links to database-formated-file
dbase = []
langs = []

# store stats on the data
linknum = 0
occnum = 0

for key,value in links.items():
    
    # increase number of links
    linknum += 1

    # get the glosses
    glossA,glossB = ids_keys[key[0]],ids_keys[key[1]]
    
    # get the key
    numA,numB = key

    # get number of occurrences
    occ = links[key]['occurrences']

    # increase number of occurrences
    occnum += occ

    # start counting by iterating over values
    evidences = links[key]['evidence']

    # iterate over evidence
    nof = [] # number of distinct language families
    nol = [] # number of distinct languages (same iso-code)
    forms = []

    for evidence in evidences:
        tmp,form = dict(evidence[0]),evidence[1]
        lang = tmp['language']
        iso = tmp['iso'].split('_')[0]
        cls = tmp['classification']
        srs = tmp['source']
        lid = tmp['id']
        var = tmp['variety']
        size = tmp['size']
        
        # try to get the link for the source
        if srs == 'ids':
            try:
                link_name = ids_web.format(ids_sources[lid])
            except KeyError:
                try:
                    link_name = ids_web.format(ids_sources[iso])
                except KeyError:
                    link_name = ids_web.format(1)

        elif srs == 'wold':
            try:
                link_name = wold_web.format(wold_sources[iso])
            except KeyError:
                link_name = wold_web.format('')

        else:
            link_name="http://www.logosdictionary.org/"
        if srs == 'ids':
            url = 'http://lingweb.eva.mpg.de/ids/'
        elif srs == 'wold':
            url = 'http://wold.livingsources.org/'
        elif srs == 'logos':
            url = 'http://www.logosdictionary.org/'

        srs = '<a href="{0}" target="_blank">{1}</a>'.format(url,srs.upper())


        if cls.lower() in ['language isolate','unclassified']:
            cls = 'unknown'

        tmp_lang = '\t'.join([lid,lang,iso,cls,srs,var,size,link_name])
        if tmp_lang in langs:
            pass
        else:
            langs.append(tmp_lang)

        # check for same language family
        if cls.split(',')[0] not in nof or cls.lower() in ['language isolate','unclassified'] :
            nof += [cls.split(',')[0]]
        
        # check for iso
        if iso not in nol:
            nol += [iso]

        # append language, iso, cls, srs to form-strings separated by ;
        forms.append('{0}:[{1}]'.format(
            lid,form))

    dbase.append(
            (
                glossA,
                glossB,
                numA,
                numB,
                str(len(nof)),
                str(len(nol)),
                '//'.join(sorted(forms))
                )
            )


out = open('output/links.sqlite3.txt','w')
for line in sorted(dbase,key=lambda x:str(x[0]+x[1]).lower()):
    out.write('\t'.join(line)+'\n')
out.close()
out = open('output/langs.sqlite3.txt','w')
for line in sorted(langs):
    out.write(line+'\n')
out.close()

os.system('rm /home/mattis/projects/scripts/clics/website/clics.de/data/clips.sqlite3')
conn = sqlite3.connect('website/clics.de/data/clips.sqlite3')
c = conn.cursor()
c.execute(
        'create table links(glossA,glossB,numA int,numB int,families int,languages int,forms);'
        )
c.execute(
        'create table langs(id,name,iso,classification,source,variety,size,link_name);'
        )
for line in sorted(dbase,key=lambda x:str(x[0]+x[1]).lower()):
    c.execute(
            'insert into links values(?,?,?,?,?,?,?);',tuple(line)
        )

for line in sorted(langs):
    c.execute(
            'insert into langs values(?,?,?,?,?,?,?,?);',tuple(line.split('\t'))
            )
conn.commit()

for v in invalid:
    print('File {0} is not valid.'.format(v))
print("Number of links: {0}".format(linknum // 2))
print("Number of occurrences: {0}".format(occnum // 2))


