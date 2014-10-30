#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


class Edge(object):

    def __init__(self, origin, dest, capability=float("inf")):
        self.capability = capability
        self.used = 0
        self.origin = origin
        self.dest = dest

    def __eq__(self, other):
        return self.origin == other.origin and self.dest == other.dest

    def __repr__(self):
        return "(" + str(self.origin) + "," + str(self.dest) + ")"


class FindingPaths(object):

    def __init__(self, graph):
        self.graph = graph
        self.paths = []

    def get_paths(self, origin, dest):
        self.s = origin
        self.t = dest
        edge_to = [None] * len(self.graph.adj)
        self.dfs(origin, [], edge_to)

    def dfs(self, origin, marked, edge_to):
        marked = list(marked)
        edge_to = list(edge_to)

        for edge in self.graph.adj[origin]:
            if edge not in marked:
                dest = edge.dest if edge.origin == origin else edge.origin
                if dest == self.t:
                    marked.append(edge)
                    path = [edge]
                    edge_from = edge_to[origin]
                    node_from = origin
                    while edge_from is not None:
                        path.insert(0, edge_from)
                        node_from = edge_from.origin if edge_from.origin != node_from else edge_from.dest
                        edge_from = edge_to[node_from]
                    if path not in self.paths:
                        self.paths.append(path)
                elif dest != self.s:
                    edge_to[dest] = edge
                    marked.append(edge)
                    self.dfs(dest, marked, edge_to)


class Graph(object):

    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.adj = []
        for i in range(num_nodes * 2 + 2):
            self.adj.append([])

    def add_edge(self, v, w):
        v1 = self.get_node_input(v)
        w1 = self.get_node_output(w)
        self.adj[v1].append(Edge(v1, w1))
        self.adj[w1].append(Edge(v1, w1))

        w2 = self.get_node_input(w)
        v2 = self.get_node_output(v)
        self.adj[w2].append(Edge(w2, v2))
        self.adj[v2].append(Edge(w2, v2))

    def get_node_input(self, v):
        # v - 1 (nodes start at 0) + 2 (source and target)
        return v + 1

    def get_node_output(self, w):
        return self.get_node_input(w) + self.num_nodes



def main():
    #data = sys.stdin.readlines()
    data = open("input03.txt").readlines()
    n_graph = int(data.pop(0).strip())
    for i in range(n_graph):
        nodes, tails, edges = data.pop(0).strip().split(" ")
        tails = int(tails)
        graph = Graph(int(nodes))
        for _ in range(int(edges)):
            d = data.pop(0).strip()
            v, w = d.split(" ")
            graph.add_edge(int(v), int(w))

        for i in range(1, int(nodes) + 1):
            input_node = graph.get_node_input(i)
            output_node = graph.get_node_output(i)
            graph.adj[0].append(Edge(0, input_node, tails))
            graph.adj[input_node].append(Edge(0, input_node, tails))
            graph.adj[output_node].append(Edge(output_node, 1, 1))
            graph.adj[output_node].append(Edge(output_node, 1, 1))

        dfs = FindingPaths(graph)
        dfs.get_paths(0, 1)

        for path in dfs.paths:
            print path

        #for path in dfs.paths:
        #    for edge in path:
        #        if not edge.capability:
        #            break
        #    else:
        #        output += 1
        #        print "output:", path
        #        for edge in path:
        #            if edge.capability < float("inf"):
        #                edge.capability -= 1







if __name__ == '__main__':
    main()
