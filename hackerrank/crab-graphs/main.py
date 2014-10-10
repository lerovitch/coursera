import sys
from get_combinations import get_combinations


class Graph:

    def __init__(self, nodes):
        self.adj = [None]
        for i in range(nodes):
            self.adj.append(list())

    def add_edge(self, v, w):
        self.adj[v].append(w)
        self.adj[w].append(v)


class CrabAlg(object):

    def __init__(self, graph, max_legs):
        self.graph = graph
        self.visited = []
        self.max_legs = max_legs
        self.queue = []
        self.solve(1)

    def solve(self, node):
        self.visited.append(node)
        for adjacent in self.graph.adj[node]:
            if adjacent not in self.visited:
                self.queue.append(adjacent)
                self.visited.append(adjacent)
        for path in self.get_paths(self.graph.adj[node], self.max_legs):
            print node, path

        if self.queue:
            self.solve(self.queue.pop(0))

    def get_paths(self, adjacents, max_legs):
        for legs in range(1, max_legs + 1):
            for i in get_combinations(adjacents, legs):
                yield i



def main():

    lines = sys.stdin.readlines()
    max_number_feet = int(lines[0].split()[1])
    nodes = int(lines[0].split()[0])
    graph = Graph(nodes)
    for line in lines[1:]:
        v, w = line.split()
        graph.add_edge(int(v), int(w))

    crab_alg = CrabAlg(graph, max_number_feet)


    



if __name__ == '__main__':
    main()
