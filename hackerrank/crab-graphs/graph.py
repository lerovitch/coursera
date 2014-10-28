import sys

def get_combinations(ls, number):
    elements = list(ls)
    result = list()
    for i, element in enumerate(elements):
        if number == 1:
            result.append([element])
        else:
            for rt in get_combinations(elements[i+1:], number - 1):
                rt.append(element)
                result.append(rt)
    return result

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



class CrabGraph(object):

    def __init__(self, graph, tails):
        self.graph = graph
        self.tails = tails

    def get_sources(self):
        sources = []
        for i, node in enumerate(self.graph.nodes):
            if len(node) >= self.tails:
                sources.append(i)
        return sources

    def get_paths(self, sources):
        paths = []
        for source in sources:
            for i in range(1, self.tails + 1):
                for combination in get_combinations(self.graph.nodes[source], i):
                    combination.append(source)
                    paths.append(combination)
        return paths


def main():
    data = sys.stdin.readlines()

    graphs = int(data.pop(0).strip())

    for i in range(graphs): 
        nodes, tails, edges = data.pop(0).strip().split(" ")
        graph = Graph(int(nodes))
        for _ in range(int(edges)):
            line = data.pop(0)
            v, w = line.strip().split(" ")
            graph.add_edge(int(v), int(w))

        crab = CrabGraph(graph, int(tails))
        sources = crab.get_sources()
        sources = range(len(graph.nodes))  # for non consecutive node ids might have a problem

        paths = crab.get_paths(sources)

        max_comb_found = 0
        max_nodes = len(sources) * int(tails)
        max_flag = False
        
        def get_paths():
            selected_nodes = set([])
            paths.sort(key=lambda x: len(x))
            for path in paths:
                if not selected_nodes.intersection(path):
                    selected_nodes = selected_nodes.union(path)

                if len(selected_nodes) == max_nodes:
                    max_flag = True
                    break
            return len(selected_nodes)

        while not max_flag and paths:
            selected = get_paths()
            max_comb_found = selected if selected > max_comb_found else max_comb_found
            paths.pop(0)


        print max_comb_found


if __name__ == "__main__":
    main()

