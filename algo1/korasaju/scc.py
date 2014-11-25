#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.setrecursionlimit(1000000)

class SCC(object):

    def __init__(self, n):
        self.adj = []
        self.rev = []
        for i in range(n+1):
            self.adj.append(list())
            self.rev.append(list())

    def add_edge(self, v, w):
        self.adj[v].append(w)
        self.rev[w].append(v)


class DFS(object):
    def __init__(self, adj):
        self.marked = [None] * len(adj)
        self.finishing = [None] * len(adj)
        self.finishing[0] = (0, 0)
        self.leader = [None] * len(adj)
        self.adj = adj
        self.t = 0

    def dfs(self, v, s):
        # marking v as explored
        self.marked[v] = 1
        self.leader[v] = s

        for node in self.adj[v]:
            if self.marked[node] is None:
                self.dfs(node, s)

        #setting finishing time
        self.t += 1
        self.finishing[v] = (v, self.t)



def main():
    lines = sys.stdin.readlines()
    n = int(lines[0])
    scc = SCC(n)

    for line in lines[1:]:
        l = line.strip().split()
        scc.add_edge(int(l[0]), int(l[1]))

    # reversing graph
    r_dfs = DFS(scc.rev)
    for i in range(n, 0, -1):
        if r_dfs.marked[i] is None:
            print "starting with", i
            r_dfs.dfs(i, i)

    r_dfs.finishing.sort(key=lambda x: x[1], reverse=True)
    for i, node in enumerate(r_dfs.finishing):
        print i, ":", node

    dfs = DFS(scc.adj)
    leader = 0
    for s, i in r_dfs.finishing[1:]:
        if dfs.marked[s] is None:
            leader += 1
            dfs.dfs(s, leader)

    leaders = [None] * len(dfs.leader)
    for i, node in enumerate(dfs.leader[1:], 1):
        try:
            leaders[node] += 1
        except:
            leaders[node] = 1

    leaders = filter(None, leaders)
    leaders.sort(reverse=True)
    for i in leaders[:5]:
        print i


if __name__ == '__main__':
    main()
