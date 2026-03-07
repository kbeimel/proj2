# BST Variation 1
# Contains values.
# Has a restructure which works like that for a scapegoat tree, but this is on-demand only.

from __future__ import annotations
from typing import List
import json

# The class for a particular node in the tree.
# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  age        : int  = None,
                  rownumbers : List[int] = [],
                  leftchild  : Node = None,
                  rightchild : Node = None,
                  parent     : Node = None,
                  iop        : Node = None,
                  ios        : Node = None):
        self.age        = age
        self.rownumbers = rownumbers
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent
        self.ios        = ios
        self.iop        = iop

# The class for a database.
class DB():
    # The __init__
    # DO NOT MODIFY!
    def __init__(self,
                 rows : List[List] = [],
                 root : Node = None
                 ):
        self.rows = rows
        self.root = root

    # Dump the rows of the database.
    # DO NOT MODIFY!
    def dump_rows(self) -> str:
        return('\n'.join( [f'{i},{l[0]},{l[1]}' for i,l in enumerate(self.rows)]))

    # Dump the index of the database.
    # DO NOT MODIFY!
    def dump_index(self) -> str:
        def _to_dict(node) -> dict:
            return {
                "age"        : node.age,
                "rownumbers" : str(node.rownumbers),
                "leftchild"  : (_to_dict(node.leftchild) if node.leftchild is not None else None),
                "rightchild" : (_to_dict(node.rightchild) if node.rightchild is not None else None),
                "parent-age" : node.parent.age if node.parent is not None else None,
                "iop-age"    : node.iop.age if node.iop is not None else None,
                "ios-age"    : node.ios.age if node.ios is not None else None
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent = 2)

    # Insert a row into the database and update the index.
    def insert(self,name: str, age: int):
        self.rows.append([name, age])
        
        if self.root is None:
            self.root = Node(age, [len(self.rows)-1], None, None, None, None, None)
            return
        
        current = self.root 
        par = None

        while current is not None :
            par = current
            if age > current.age :
                current=current.rightchild
            elif age < current.age :
                current= current.leftchild 
            elif current.age == age : 
                current.rownumbers.append(len(self.rows)-1)
                return
        nunode = Node(age, [(len(self.rows)-1)], None, None, par, None, None)
        if par.age > age :
            par.leftchild = nunode
            par.leftchild.ios = par
        else :
            par.rightchild = nunode   
            par.rightchild.iop = par                  



    # Delete a row from the database and update the index.
    def delete(self,name:str):
        # The next line is a placeholder to make sure the code runs.
        placeholder = True

    # Use the index to find a the people whose age is specified.
    def people_single(self,age:int):
        # Replace these lines.
        # d should be the depth of the node where the names are found.
        # n should be the list of names.
        d = 0
        n = []
        # Return the object.
        n.sort()
        r = {'depth' : d,'names': n }
        return json.dumps(r,indent = 2)

    # Use the index to find a the people whose age is in the range given.
    def people_range(self,age_min:int,age_max:int):
        # Replace these lines.
        # d should be the number of nodes where the names are found.
        # n should be the list of names.
        d = 0
        n = []
        # Return the object.
        n.sort()
        r = {'nodecount' : d,'names': n }
        return json.dumps(r,indent = 2)