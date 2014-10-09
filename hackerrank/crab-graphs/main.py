import sys


class Graph:

    def __init__(self, nodes):
        self.adj = [None]
        for i in range(nodes):
            self.adj.append(list())

    def add_edge(self, v, w):
        self.adj[v].append(w)
        self.adj[w].append(v)


class CrabAlg(object):

    def __init__(self, graph):
        self.graph = graph
        self.solve(1)
        self.visited = []
        self.max = 0

    def solve(self, node):
        self.visited.append(node)
        queue = []
        for adjacent in self.graph.adj[node]:
            if adjacent not in self.visited:
                queue.append(adjacent)
                self.visited.append(adjacent)




def main():

    lines = sys.stdin.readlines()
    max_number_feet = lines[0].split()[1]
    nodes = lines[0].split()[0]
    graph = Graph(nodes)
    for line in lines[1:]:
        print line.strip()
    



if __name__ == '__main__':
    main()
