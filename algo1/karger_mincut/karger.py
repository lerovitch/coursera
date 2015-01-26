#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import random


class KargerGraph():
    
    def __init__(self, nodes, lines):
        """docstring for __init__"""

        self.adj = [[]]
        self.selectable = range(1, nodes + 1)
        for _ in range(nodes):
            self.adj.append([])

        for i in lines:
            i = i.split()
            i = [int(x) for x in i]
            index = i.pop(0)
            self.adj[index] = i

    def remove_element_adjlist(self, index, element):
        try:
            while True:
                self.adj[index].remove(element)
        except ValueError:
            pass

    def mincut(self):
        while len(self.selectable) > 2:
            d_node = random.choice(self.selectable)
            self.selectable.remove(d_node)
            o_node = random.choice(self.adj[d_node])

            # add loops from d_node
            for edge in self.adj[d_node]:
                if edge != o_node:  # remove self loops
                    self.adj[o_node].append(edge)
                    self.adj[edge].append(o_node)
                    self.remove_element_adjlist(edge, d_node)  # remove self loops from o_node
            self.remove_element_adjlist(o_node, d_node)  # remove self loops from o_node

        return len(self.adj[self.selectable[0]])



def main():
    """docstring for main"""

    lines = sys.stdin.readlines()
    #lines = open("mincut.txt").readlines()
    nodes = int(lines.pop(0))
    mincut = float("inf")
    for _ in range(nodes):
        graph = KargerGraph(nodes, lines)
        value = graph.mincut()
        if value < mincut:
            mincut = value

    print mincut






if __name__ == '__main__':
    main()

    


