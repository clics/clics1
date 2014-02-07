import json

fh = json.load(open('data.json'))

nodes = fh['nodes']
links = fh['links']

idByName = {id:'root.group' + str(n['group']) + '.' + str(n['name']) for id,n in enumerate(nodes)}

entries = list()

for count,node in enumerate(nodes):
	source_links = [f for f in links if f['source'] == count]
	name = 'root.group' + str(node['group']) + '.' + str(node['name'])
	imports = list()
	for s in source_links:
		weight = s['value']
		edge = idByName[s['target']]
		imports.append({'edge': edge, 'weight': weight})
	currEntry = {'name':name,'imports':imports}
	entries.append(currEntry)
	
	
oh = open('d2.json','w')
oh.write(json.dumps(entries))
oh.close()