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

    def infix(self, node: Node, index):
        if node is None:
            return
        node.rownumbers = [r - 1 if r > index else r for r in node.rownumbers]
        self.infix(node.leftchild, index)
        self.infix(node.rightchild, index)

    def remove_node(self, node: Node):
        if node.leftchild is not None and node.rightchild is not None:
            ciop = node.iop
            if ciop:
                node.age = ciop.age
                node.rownumbers = ciop.rownumbers
                node.iop= ciop.iop
                self.remove_node(ciop)
                return
        else:
            kid = node.leftchild if node.leftchild is not None else node.rightchild
            if node.parent:
                if node.parent.leftchild == node:
                    node.parent.leftchild = kid
                else:
                    node.parent.rightchild = kid
            else: 
                self.root = kid
            if kid:
                kid.parent = node.parent

            if node.iop:
                node.iop.ios = node.ios
            if node.ios:
                node.ios.iop = node.iop

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
        if par is not None :
            if par.age > age :
                par.leftchild = nunode
                nunode.ios = par
                nunode.iop = par.iop
                if par.iop is not None :
                    par.iop.ios = nunode
                par.iop = nunode
            else :
                par.rightchild = nunode   
                nunode.iop = par
                nunode.ios = par.ios
                if par.ios is not None :
                    par.ios.iop = nunode      
                par.ios = nunode            



    # Delete a row from the database and update the index.
    def delete(self,name:str):
        ind = None
        age = None
        for i, row in enumerate(self.rows):
            if row[0] == name:
                (ind, age) = (i, row[1])
                break
        if ind is not None:
            current = self.root 

            while current is not None :
                if age == current.age:
                    if ind in current.rownumbers:
                        current.rownumbers.remove(ind)
                    if not current.rownumbers:
                        self.remove_node(current)
                    break
                elif age > current.age :
                    current = current.rightchild
                else :
                    current = current.leftchild
            self.rows.pop(ind)
            if self.root:
                self.infix(self.root, ind)

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