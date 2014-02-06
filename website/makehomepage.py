# author   : Johann-Mattis List
# email    : mattis.list@gmail.com
# created  : 2013-02-02 13:52
# modified : 2013-08-29 09:50
"""
Script produces output for the clips-website.
"""

__author__="Johann-Mattis List"
__date__="2013-08-29"

import re
from glob import glob
from datetime import datetime
import json

template = open('templates/content.php').read()

today = datetime.today().strftime('%h. %d, %Y, %H:%M CET')

infiles = glob('files/*.php')
conf = json.load(open('templates/clips.json'))

for infile in infiles:
    inf = open(infile).read()
    
    try:
        sidebar = re.findall(r'<!-- SIDEBAR ([a-zA-Z]*?) -->',inf)
        sidebar = sidebar[0]
    except:
        sidebar = 'about'

    sidebar = open('templates/'+sidebar+'.php').read()
    
    name = infile.replace('files/','clics.de/')
    filename = infile.replace('files/','').replace('.php','')
    
    for f in conf['pages']:
        if f == filename:
            conf['pages'][f] = 'active'
        else:
            conf['pages'][f] = 'inactive'
    
    sidebar = sidebar.format(**conf['pages'])

    f = open(name,'w')
    f.write(template.format(
        content = inf,
        update = today,
        sidebar = sidebar
        )
        )
    f.close()
    f = open(name.replace('clics.de/','php/'),'w')
    f.write(template.format(
        content = inf,
        update = today,
        sidebar = sidebar
        )
        )
    f.close()



