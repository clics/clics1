import networkx as nx
from networkx.readwrite import json_graph
import json

def gml2json(infile):

    graph = nx.read_gml(infile)
    
    # delete all nodes
    for n,d in graph.nodes(data=True):
        del d['id']

    # convert to json
    jdata = json_graph.adjacency_data(graph)

    # write to file
    f = open(infile.replace('gml','json'),'w')
    json.dump(jdata,f)
    f.close()
    print("[i] Conversion successful...")

def graph2json(graph,filename):

    # convert to json
    jdata = json_graph.adjacency_data(graph)

    # write to file
    f = open(filename+'.json','w')
    json.dump(jdata,f)
    f.close()

