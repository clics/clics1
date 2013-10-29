CLiCs
=====

Database of Cross-Linguistic Colexifications

### Create Network from Data

Use the link.py script to create a network from all wordlists files in the folder "wordlists". The data here is no real network, but rather a collection of all links that is stored in a format suitable for accessing it on the website. The script also automatically generates an updated sqlite3 file that is accessed on the website using the php code in the website-folder.

### Update Website

All essential files for the website that can dynamically be changed are in the folder website/files. In order to update the website, update the files there manually and then run the "makehomepage.py"-script that will use the templates and the content in the files and create a new version of the website. This version is accessible via the folder clics.de/.

### Export Information on Links to GML and JSON

In order to retrieve a GML-output file, just use gml.py without any arguments. The script reads in the graph contained in "links.sqlite3.txt" and converts it to gml-format. Additionally, the script adds a tagging of IDS concepts: All items present in the Swadesh-100 list will be tagged accordingly.

In addition to pure gml-export, the script automatically converts the gml-graph to json. This is useful for applications that make use of JavaScript or the like.

### Get Basic Statistics on the Data

run "get\_data.py" in order to retrieve some basic statistics regarding the data in our sample.

### Carry out community detection analysis

Use the script "communities.py" to carry out such an analysis. Problem is only, that the analyses in igraph are not that good, as expected: the "leading" methods, like "infomap" yield far too many large communities, where we would like to have subsets of no more than, say, 30 nodes, or so. The current output of infomap is available in communities/-folder. I'll try to compare it with another analysis later, but the problem is that alternative analyses run rather slow, and it takes some time to run on my PC.

### Current plans for code to appear on this page

* code for computation of the whole network (preferably as json-like format in output)
* the computed full network
* code for computation of community clustering with help of igraph
* a csv-list containing node and community for all communities in the network
* a labelling for all communities (preferably the centroid or how that's called for each community)
* a csv-list with semantic fields of IDS and nodes belonging to the fields

