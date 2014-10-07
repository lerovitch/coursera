import sys


class Graph(object):

    def __init__(self, vertex):
        self.nodes = []
        for i in range(vertex):
            self.nodes.append(list())

    def add_edge(self, v, w):
        v -= 1
        w -= 1
        self.nodes[v].append(w)
        self.nodes[w].append(v)


# We need to find the number of child nodes that each node has.
# The easiest way is to iterate recursively over all child nodes until 
# a leave node is found, then start sum it up
#
class DFS(object):

    def __init__(self, graph):
        self.marked = [False] * len(graph.nodes)
        self.graph = graph
        self.childs = [0] * len(graph.nodes)
        self.cuts = 0
        self.dfs(0, graph.nodes[0])

    def dfs(self, v, nodes):
        self.marked[v] = True
        childs = 0
        for w in nodes:
            if not self.marked[w]:
                childs +=  1 + self.dfs(w, self.graph.nodes[w])
        self.childs[v] = childs
        if childs > 0 and childs % 2 != 0:
            self.cuts += 1
        return childs


def print_nodes(nodes):
    return  [x+1 for x in nodes]

def main():
    data = sys.stdin.readlines()
    #data = open("input.txt").readlines()
    nodes, edges = data[0].split(" ")
    graph = Graph(int(nodes))
    for line in data[1:]:
        v, w = line.split(" ")
        graph.add_edge(int(v), int(w))

    dfs = DFS(graph)
    print dfs.cuts - 1

if __name__ == "__main__":
    main()

