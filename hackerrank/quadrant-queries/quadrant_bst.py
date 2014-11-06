#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import random


BLACK = 0
RED = 1
class Node(object):

    def __init__(self, value=None, parent=None):
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None
        self.color = BLACK
        self.height = 0

    def size(self):
        left_size = self.left.size() if self.left else 0
        right_size = self.right.size() if self.right else 0
        return left_size + right_size + 1

    def insert(self, node):
        if not isinstance(node, Node):
            node = Node(node)

        if self.value is None:
            self.value = node.value
            self.color = RED

        elif self.value >= node.value:
            if self.left:
                self.left = self.left.insert(node)
            else:
                self.left = Node(parent=self).insert(node)

        elif self.value < node.value:
            if self.right:
                self.right = self.right.insert(node)
            else:
                node.parent = self
                self.right = Node(parent=self).insert(node)

        h = self

        if h.left and h.left.left and h.left.color == RED and h.left.left.color == RED:
            h = self.rotate_right()

        if h.right and h.right.color == RED and ((h.left and h.left.color == BLACK) or not h.left):
            h = self.rotate_left()

        if h.right and h.right.color == RED and h.left and h.left.color == RED:
            h.flip_colors()

        if h.parent is None:
            h.color = BLACK

        return h

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
            if self.parent.right == self and self.right:
                self.parent.right = self.right
                self.right.parent = self.parent
            elif self.parent.left == self and self.right: 
                self.parent.left = self.right
                self.right.parent = self.parent

            elif self.parent.right == self and self.left: 
                self.parent.right = self.left
                self.left.parent = self.parent
            elif self.parent.left == self and self.left: 
                self.parent.left = self.left
                self.left.parent = self.parent
        else:
            self.value = (self.right and self.right.value) or (self.left and self.left.value)
            self.right = None
            self.left = None

    def min(self):
        if self.left:
            return self.left.min()
        else:
            return self

    def rotate_left(self):
        """rotate a node that has a right child as red"""
        assert self.right.color == RED
        x = self.right
        self.right = x.left
        x.left = self
        x.color = self.color
        x.parent = self.parent
        self.parent = x
        self.color = RED
        return x

    def rotate_right(self):
        """rotate a node that has a left child as red"""
        assert self.left.color == RED
        x = self.left
        x.parent = self.parent
        self.left = x.right
        x.right = self
        self.parent = x
        x.color = self.color
        self.color = RED
        return x

    def flip_colors(self):
        assert self.color != RED
        assert self.left.color == RED
        assert self.right.color == RED
        self.color = RED
        self.left.color = BLACK
        self.right.color = BLACK

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
                self.delete_min()
                deleted = 1
            elif (not self.left and self.right) or (not self.right and self.left):
                self.delete_wone_children()
                deleted = 1
            else:
                successor = self.right.min()
                self.delete(successor.value)
                self.value = successor.value
        return deleted

    def get_height(self):
        nodes = []
        if self.left:
            nodes.append(self.left)
            self.left.height = self.height + 1
        if self.right:
            nodes.append(self.right)
            self.right.height = self.height + 1

        while nodes:
            next = nodes.pop(0)
            if next.left:
                nodes.append(next.left)
                next.left.height = next.height + 1
            if next.right:
                nodes.append(next.right)
                next.right.height = next.height + 1
        return next.height

    def __repr__(self):
        left = str(self.left.value) if self.left else ""
        right = str(self.right.value) if self.right else ""
        color = "red" if self.color == RED else "black"
        return str(self.value) + " " + color + " l:" + left + " r:" + right


node = Node(10)
node = node.insert(Node(5))
node = node.insert(Node(20))
node = node.insert(Node(18))
node = node.insert(Node(19))
node = node.insert(Node(21))
node.get_height()
print node.size()

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
        #ls_quadrant_1.remove(value)
        #value = random.choice(ls_quadrant_1)
        value = ls_quadrant_1.pop()
        quadrant_1 = quadrant_1.insert(value)
    while ls_quadrant_2:
        #value = random.choice(ls_quadrant_2)
        #ls_quadrant_2.remove(value)
        value = ls_quadrant_2.pop()
        quadrant_2 = quadrant_2.insert(value)
    while ls_quadrant_3:
        #value = random.choice(ls_quadrant_3)
        #ls_quadrant_3.remove(value)
        value = ls_quadrant_3.pop()
        quadrant_3 = quadrant_3.insert(value)
    while ls_quadrant_4:
        #value = random.choice(ls_quadrant_4)
        #ls_quadrant_4.remove(value)
        value = ls_quadrant_4.pop()
        quadrant_4 = quadrant_4.insert(value)

    print "q1: " + str(quadrant_1.size())
    print "q2: " + str(quadrant_2.size())
    print "q3: " + str(quadrant_3.size())
    print "q4: " + str(quadrant_4.size())
    print "q1: " + str(quadrant_1.get_height())
    print "q2: " + str(quadrant_2.get_height())
    print "q3: " + str(quadrant_3.get_height())
    print "q4: " + str(quadrant_4.get_height())

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

                print "q1 inserting:", i
                quadrant_1 = quadrant_1.insert(i)
                if i == 2980:
                    #import ipdb; ipdb.set_trace()
                    pass
                quadrant_4.delete(i)
                print "q4 deleted:", i, quadrant_4.get(2982).parent if quadrant_4.get(2982) else None, quadrant_4.get(2982)
            for i in to_2:
                print "q2 inserting:", i
                quadrant_2 = quadrant_2.insert(i)
                print "q3 deleting:", i
                quadrant_3.delete(i)
            for i in to_3:
                print "q3 inserting:", i
                quadrant_3 = quadrant_3.insert(i)
                print "q2 deleting:", i
                quadrant_2.delete(i)
            for i in to_4:
                quadrant_4 = quadrant_4.insert(i)
                if i == 2982:
                    pass

                print "q4 inserted:", i, quadrant_4.get(2982).parent if quadrant_4.get(2982) else None, quadrant_4.get(2982)
               # print "q4 inserted:", i, quadrant_4.get(2982)
                print "q1 deleting:", i
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
    
