#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

class Edge(object):

    def __init__(self, origin, dest, capability=float("inf")):
        self.capability = capability
        self.used = 0
        self.origin = origin
        self.dest = dest

    def __repr__(self):
        return "(" + str(self.origin) + "," + str(self.dest) + ")"


class DFS(object):
    def __init__(self, graph):
        self.graph = graph

    def dfs(self, s, t):
        self.edge_to = []
        self.paths = []
        self.s = s
        self.t = t
        for i in range(2 + 2*self.graph.num_nodes):
            self.edge_to.append(None)
        self.get_paths(s)

    def get_paths(self, s):

        import ipdb; ipdb.set_trace()
        for i_edge in self.graph.adj[s]:
            backward = True if i_edge.dest == s else False
            node = i_edge.dest if not backward else i_edge.origin
            print s, i_edge, node
            if node == self.t:
                path = [i_edge]
                prev_edge = self.edge_to[s]
                path.append(prev_edge)
                prev_backward = True if prev_edge.origin == node else False
                prev_origin = prev_edge.origin if not prev_backward else prev_edge.dest
                while prev_origin != self.s:
                    prev_edge = self.edge_to[prev_origin]
                    path.append(prev_edge)
                self.paths.append(path[::-1])
                break

            self.edge_to[node] = i_edge
            self.get_paths(node)



class Graph(object):

    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.adj = []
        for i in range(num_nodes*2 + 2):
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

        dfs = DFS(graph)
        dfs.dfs(0,1)

        output = 0

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

        print output






if __name__ == '__main__':
    main()
