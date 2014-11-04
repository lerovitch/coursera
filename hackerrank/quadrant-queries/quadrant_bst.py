#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import random

class Node(object):

    def __init__(self, value=None, parent=None):
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None
        self.size = 1 if value else 0

    def insert(self, node):
        if self.value is None:
            if not isinstance(node, Node):
                self.value = node
            else:
                self.value = node.value
            return 

        if not isinstance(node, Node):
            node = Node(node)

        self.size += 1
        if self.value >= node.value:
            if self.left:
                self.left.insert(node)
            else:
                self.left = node
                node.parent = self
        elif self.value < node.value:
            if self.right:
                self.right.insert(node)
            else:
                self.right = node
                node.parent = self

    def get(self, value):
        if self.value == value:
            return self
        elif self.value >= value:
            if self.left:
                return self.left.get(value)
        elif self.right:
            return self.right.get(value)
        return None

    def delete_min(self):
        if self.parent:
            if self.parent.right == self:
                self.parent.right = None
            else:
                self.parent.left = None
        else:
            self.value = None
            self.right = None
            self.left = None

    def delete_wone_children(self):
        if self.parent:
            if self.right:
                self.parent.right = self.right
                self.right.parent = self.parent
            else:
                self.parent.left = self.left
                self.left.parent = self.parent
        else:
            self.value = (self.right and self.right.value) or (self.left and self.left.value)
            self.right = None
            self.left = None
        print "wone", self.parent
        print "wone", self.left
        print "wone", self.right


    def min(self):
        if self.left:
            return self.left.min()
        else:
            return self

    def interval(self, i_min, i_max, ls=None): 
        if ls is None:
            ls = []
        if self.left and self.left.value >= i_min:
            self.left.interval(i_min, i_max, ls)
        if i_max >= self.value and i_min <= self.value:
            ls.append(self.value)
        if self.right and self.right.value <= i_max:
            self.right.interval(i_min, i_max, ls)
        return ls

    def inorder(self, ls): 
        if self.left:
            self.left.inorder(ls)
        ls.append(self.value)
        if self.right:
            self.right.inorder(ls)
        return ls

    def delete(self, value):
        deleted = 0
        if self.right and self.value < value:
            deleted = self.right.delete(value)

        elif self.left and self.value > value:
            deleted = self.left.delete(value)
        elif self.value == value:
            if not self.left and not self.right:
                print "deleting no children", self
                self.delete_min()
                deleted = 1
            elif (not self.left and self.right) or (not self.right and self.left):
                print "deleting one children", self
                self.delete_wone_children()
                deleted = 1
            else:
                print "deleting two children", self
                successor = self.right.min()
                print "successor", successor
                if successor.value == self.value:
                    import ipdb; ipdb.set_trace()
                self.delete(successor.value)
                self.value = successor.value
        self.size -= deleted
        return deleted

    def __repr__(self):
        left = str(self.left.value) if self.left else ""
        right = str(self.right.value) if self.right else ""
        return "(" + str(self.value) + ")" + " size: " + str(self.size) + " left:" + left + " right:" + right


#node = Node(10)
#node.insert(Node(5))
#node.insert(Node(20))
#node.insert(Node(15))
#node.insert(Node(25))
#node.insert(Node(19))
#node.insert(Node(24))



def main():
    """docstring for main"""
    lines = open("input03.txt").readlines()
    #lines = sys.stdin.readlines()

    # reading points
    n_points = int(lines.pop(0))
    points = []

    ls_quadrant_1 = []
    ls_quadrant_2 = []
    ls_quadrant_3 = []
    ls_quadrant_4 = []

    quadrant_1 = Node()
    quadrant_2 = Node()
    quadrant_3 = Node()
    quadrant_4 = Node()

    for i in range(1, n_points + 1):
        point = [int(x) for x in lines.pop(0).split()]
        if point[0] < 0:
            if point[1] < 0:
                ls_quadrant_3.append(Node(i))

                #if quadrant_3 is None:
                #    quadrant_3 = Node(i)
                #else:
                #    quadrant_3.insert(Node(i))
            else:
                ls_quadrant_2.append(Node(i))
                #if quadrant_2 is None:
                #    quadrant_2 = Node(i)
                #else:
                #    quadrant_2.insert(Node(i))
        else:
            if point[1] < 0:
                ls_quadrant_4.append(Node(i))
                #if quadrant_4 is None:
                #    quadrant_4 = Node(i)
                #else:
                #    quadrant_4.insert(Node(i))
            else:
                ls_quadrant_1.append(Node(i))
                #if quadrant_1 is None:
                #    quadrant_1 = Node(i)
                #else:
                #    quadrant_1.insert(Node(i))
    while ls_quadrant_1:
        value = random.choice(ls_quadrant_1)
        ls_quadrant_1.remove(value)
        quadrant_1.insert(value)
    while ls_quadrant_2:
        value = random.choice(ls_quadrant_2)
        ls_quadrant_2.remove(value)
        quadrant_2.insert(value)
    while ls_quadrant_3:
        value = random.choice(ls_quadrant_3)
        ls_quadrant_3.remove(value)
        quadrant_3.insert(value)
    while ls_quadrant_4:
        value = random.choice(ls_quadrant_4)
        ls_quadrant_4.remove(value)
        quadrant_4.insert(value)

    
    print quadrant_1.size
    print quadrant_2.size
    print quadrant_3.size
    print quadrant_4.size



    n_queries = int(lines.pop(0))
    queries = []
    for _ in range(n_queries):
        query = lines.pop(0).split()
        print query
        query[1] = int(query[1])
        query[2] = int(query[2])
        if query[0] == "X":
            to_4 = quadrant_1.interval(query[1], query[2])
            to_3 = quadrant_2.interval(query[1], query[2])
            to_2 = quadrant_3.interval(query[1], query[2])
            to_1 = quadrant_4.interval(query[1], query[2])
            for i in to_1:
                print "inserting", i
                quadrant_1.insert(i)
                print "deleting", i
                quadrant_4.delete(i)
            for i in to_2:
                quadrant_2.insert(i)
                quadrant_3.delete(i)
            for i in to_3:
                quadrant_3.insert(i)
                quadrant_2.delete(i)
            for i in to_4:
                quadrant_4.insert(i)
                quadrant_1.delete(i)

        elif query[0] == "Y":
            to_2 = quadrant_1.interval(query[1], query[2])
            to_1 = quadrant_2.interval(query[1], query[2])
            to_4 = quadrant_3.interval(query[1], query[2])
            to_3 = quadrant_4.interval(query[1], query[2])
            for i in to_1:
                quadrant_1.insert(i)
                quadrant_2.delete(i)
            for i in to_2:
                quadrant_2.insert(i)
                quadrant_1.delete(i)
            for i in to_3:
                quadrant_3.insert(i)
                quadrant_4.delete(i)
            for i in to_4:
                quadrant_4.insert(i)
                quadrant_3.delete(i)


        elif query[0] == "C":
            results = []
            results.append(str(len(quadrant_1.interval(query[1], query[2]))))
            results.append(str(len(quadrant_2.interval(query[1], query[2]))))
            results.append(str(len(quadrant_3.interval(query[1], query[2]))))
            results.append(str(len(quadrant_4.interval(query[1], query[2]))))
            print " ".join(results)
            



if __name__ == '__main__':
    main()
    
