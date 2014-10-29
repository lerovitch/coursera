import sys

class Graph(object):

    def __init__(self, nodes):
        self.adj = []
        for _ in range(nodes):
            self.adj.append([])

    def add_edge(self, v, w):
        v = int(v) - 1
        w = int(w) - 1
        self.adj[v].append((v, w))
        self.adj[w].append((v, w))


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
                dest = edge[1] if edge[0] == origin else edge[0]
                if dest == self.t:
                    marked.append(edge)
                    path = [edge]
                    edge_from = edge_to[origin]
                    while edge_from is not None:
                        path.insert(0, edge_from)
                        node_from = edge_from[0] if edge_from[0] != origin else edge_from[1]
                        edge_from = edge_to[node_from]
                    self.paths.append(path)
                elif dest != self.s:
                    edge_to[dest] = edge
                    marked.append(edge)
                    self.dfs(dest, marked, edge_to)


def main():
    lines = open("paths.txt").readlines()
    nodes, edges = lines.pop(0).split(" ")
    graph = Graph(int(nodes))
    for _ in range(int(edges)):
        v, w = lines.pop(0).split(" ")
        graph.add_edge(v, w)

    f_paths = FindingPaths(graph)
    f_paths.get_paths(0, 3)

    for path in f_paths.paths:
        print path



if __name__ == '__main__':
    main()


