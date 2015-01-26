"""
This script contains the Dijstra's algorithm implementation. For each iteration, the minimum weight will be computed
among all edges (no heaps implementation).
The input of the script is a file containing all the vertex relationships with their edge legths
e.g

1  3,23  4,12

The previous row would indicate that there is an edge from 1 to 3 with length 23 and an edge from 1 to 4 of length 12
The script will return the shortest-path distance of a list of nodes
"""
import argparse

not_found_path_distance = 1000000


def parse_file(file_to_parse):
    """
    Will contruct a dict of the graph in the way: {source_vertex : {dest_vertex: length}}
    """
    with open(file_to_parse, 'r') as f:
        data = f.readlines()
        g = {}
        nodes = set([])
        for x in data:
            elems = x.split('\t')
            g[int(elems[0])] = {}
            nodes.add(int(elems[0]))
            for elem in elems:
                if ',' in elem:
                    dest_info = elem.split(',')
                    nodes.add(int(dest_info[0]))
                    g[int(elems[0])][int(dest_info[0])] = int(dest_info[1])
        return g, nodes

def dijstra(g, initial_vertex, destination_vertices, v):
    """
    Returns the list of distances between the initial_vertex and the list of destinations
    """
    g_v = g.copy()
    x = set([initial_vertex])
    a = {initial_vertex: 0}
    found_vertices = []
    while x != v:
        minimum = not_found_path_distance
        minimum_dest = None
        for s_vert in x:
            for d_vert, length in g_v.get(s_vert, {}).items():
                if a[s_vert] + length < minimum and d_vert not in x:
                    minimum = a[s_vert] + length
                    minimum_dest = d_vert
        a[minimum_dest] = minimum
        x.add(minimum_dest)
        if minimum_dest in destination_vertices:
            found_vertices.append(minimum_dest)
        if len(destination_vertices) == len(found_vertices):
            break
    return [a.get(x, not_found_path_distance) for x in destination_vertices]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a file with graph in adjacency lists representation')
    parser.add_argument('--f', dest='file_to_parse',
        help='File to parse')

    args = parser.parse_args()

    g, nodes = parse_file(args.file_to_parse)
    demanded_vertices = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]
    result = dijstra(g, 1, demanded_vertices, nodes)
    print result
