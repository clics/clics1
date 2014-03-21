from lingpyd import *
import json

def nwk2json(treestring,filename=""):
    
    tree = LoadTree(treestring=treestring)
    d = dict(
            name = tree.Name,
            children = []
            )

    this_dict = d
    
    queue = [(tree,this_dict)]

    while queue:
        
        # get the children of the tree
        this_tree,this_dict = queue.pop(0)
        
        # get the name of the children
        names = [child.Name for child in this_tree.Children]
        
        for child,name in zip(this_tree.Children,names):
            new_tree = dict(
                    name = name,
                    children = []
                    )

            this_dict['children'] += [new_tree]

            queue += [(child,new_tree)]
    
    if filename:
        f = open(filename+'.json','w')
        json.dump(d,f)
        f.close()
    else:
        return json.dumps(d)
    


