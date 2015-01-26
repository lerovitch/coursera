#!/usr/bin/env python
# -*- coding: utf-8 -*-

MAX = 1000000

class WeightedGraph(object):

    def __init__(self, n):
        self.adj = [None] * (n + 1)


def main():
    #lines = open("mini.txt").readlines()
    lines = open("dijkstraData.txt").readlines()
    graph = {}
    for line in lines:
        sp = line.split()
        i = int(sp[0])
        adj_el = [tuple([int(x.split(",")[0]), 
                        int(x.split(",")[1])]) for x in sp[1:]]
        assert i != 0
        graph[i] = adj_el

    A = [0] * (len(graph) + 1)  # computes shortest path distances
    X = []  # vertex processed so far

    X.append(1)

    # edges = { node: (weight, origin)}

    while len(X) != len(graph):
        minimum = 1000000
        next = 0
        origin = 0
        for p_node in X:
            for dest, weight in graph[p_node]:
                if dest not in X and (weight + A[p_node]) < minimum:
                    minimum = weight + A[p_node]
                    next = dest
                    origin = p_node
        if next == 0:
            break
        X.append(next)
        A[next] = minimum


    results = [str(A[i]) for i in [7,37,59,82,99,115,133,165,188,197]]
    print ",".join(results)
    results = [A[i] for i in [7,37,59,82,99,115,133,165,188,197]]
    print results
    print [2599, 2610, 2947, 2052, 2367, 2399, 2029, 2442, 2505, 3068]


    



if __name__ == '__main__':
    main()
