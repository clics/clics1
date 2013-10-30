# Use simple shell commands to store the workflow of the scripts in this project.
# Note that the command "python" corresponds to "python3", so eventually, this point needs to be adapted, depending on local preferences

# get all links in the data in wordlists/
python links.py wordlists/

# get basic statistics
python stats.py

# get gml graph of the data
python gml.py

# get communities using infomap
python communities.py infomap
