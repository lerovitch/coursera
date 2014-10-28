

class Graph(object):

    def __init__(self, nodes):
        self.adj = []
        for _ in range(nodes):
            self.adj.append([])

    def add_edge(self, v, w):
        v = int(v) - 1
        w = int(w) - 1
        self.adj[v].append(w)
        self.adj[w].append(v)


class FindingPaths(object):

    def __init__(self, graph):
        self.graph = graph

    def get_paths(self, origin, dest):
        self.t = dest
        for node in self.graph.adj[origin]:
        pass

    def dfs(self, origin):




def main():
    import sys
    lines = open("paths.txt").readlines()
    nodes, edges = lines.pop(0).split(" ")
    graph = Graph(int(nodes))
    for _ in int(edges):
        v, w = lines.pop(0).split(" ")
        graph.add_edge(v, w)






