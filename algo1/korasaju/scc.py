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
        self.leaders = [None] * len(adj)
        self.adj = adj
        self.t = 0
        self.leader = None

    def dfs(self, v):
        # marking v as explored
        assert v != 0
        self.marked[v] = 1
        self.leaders[v] = self.leader

        try:
            for node in self.adj[v]:
                if self.marked[node] is None:
                    assert node <= 875714
                    self.dfs(node)
        except IndexError, e:
            print e, v

        #setting finishing time
        self.t += 1
        self.finishing[v] = (v, self.t)



def main():
    #lines = sys.stdin.readlines()
    lines = open("SCC.txt").readlines()
    n = int(lines[0])
    scc = SCC(n)

    for line in lines[1:]:
        l = line.strip().split()
        scc.add_edge(int(l[0]), int(l[1]))

    # reversing graph
    r_dfs = DFS(scc.rev)
    for i in range(n, 0, -1):
        if r_dfs.marked[i] is None:
            r_dfs.dfs(i)
    print r_dfs.finishing.pop(0)
    r_dfs.finishing.sort(key=lambda x: x[1], reverse=True)

    dfs = DFS(scc.adj)
    for s, i in r_dfs.finishing:
        assert s <= 875714
        if dfs.marked[s] is None:
            dfs.leader = s
            dfs.dfs(s)

    assert dfs.leaders[0] is None
    assert dfs.marked[0] is None

    leaders = [None] * len(dfs.leaders)
    for i, node in enumerate(dfs.leaders[1:], 1):
        try:
            leaders[node] += 1
        except:
            leaders[node] = 1

    leaders = filter(None, leaders)
    leaders.sort(reverse=True)
    print leaders[:10], sum(leaders)


if __name__ == '__main__':
    main()
