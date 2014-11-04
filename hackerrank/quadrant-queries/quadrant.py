#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

class Node(object):

    def __init__(self, value=None, parent=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

    def insert(self, node):
        if self.value < node.value:
            if left:
                left.insert(node)
            else:
                self.left = node
                node.parent = self
        elif self.value >= node.value:
            if right:
                right.insert(node)
            else:
                self.right = node
                node.parent = self



def main():
    """docstring for main"""
    #lines = open("sample.txt").readlines()
    lines = sys.stdin.readlines()

    # reading points
    n_points = int(lines.pop(0))
    points = []


    for _ in range(n_points):
        point = [int(x) for x in lines.pop(0).split()]
        points.append(point)

    n_queries = int(lines.pop(0))
    queries = []
    for _ in range(n_queries):
        query = lines.pop(0).split()
        query[1] = int(query[1])
        query[2] = int(query[2])
        if query[0] == "C":
            query.extend([0] * 4)
        queries.append(query)


    # algorithm

    for i, p in enumerate(points, 1):
        print i
        for q in queries:
            if q[0] == "X" and i >= q[1] and i <= q[2]:
                p[1] = -p[1]
            if q[0] == "Y" and i >= q[1] and i <= q[2]:
                p[0] = -p[0]
            if q[0] == "C" and i >= q[1] and i <= q[2]:
                if p[0] > 0:
                    if p[1] > 0:
                        q[3] += 1
                    else:
                        q[6] += 1
                else:
                    if p[1] > 0:
                        q[4] += 1
                    else:
                        q[5] += 1

    for q in queries:
        if q[0] == "C":
            print " ".join([str(x) for x in q[3:]])

        


if __name__ == '__main__':
    main()
    
