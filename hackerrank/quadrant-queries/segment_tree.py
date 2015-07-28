import math
import sys

QUAD_1 = 0
QUAD_2 = 1
QUAD_3 = 2
QUAD_4 = 3

level = -1
zero = -1


class Query(object):
    def __init__(self, init, end, tx, ty):
        self.init = init
        self.end = end
        self.tx = tx
        self.ty = ty

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Q({0}, {1}) {2} {3}'.format(self.init, self.end, self.tx, self.ty)

class Segment(object):

    def __init__(self, init, end, quads=[]):
        self.init = init
        self.end = end
        self.quads = quads
        self.n = -1

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'S{3} ({0}, {1}) {2}'.format(self.init, self.end, self.quads, self.n)


def get_interval_from_coords(cx, cy):
    if cx < 0:
        if cy < 0:
            return QUAD_3
        else:
            return QUAD_2
    else:
        if cy < 0:
            return QUAD_4
        else:
            return QUAD_1


def build_tree(points):
    global level, zero
    level = int(math.ceil(math.log(len(points), 2)))
    zero = 2 ** level
    tree = [None] * (2 ** (level + 1))
    

    def _build_tree(i):
        if i < zero:
            leftchild = 2*i
            rightchild = 2*i + 1
            _build_tree(leftchild)
            _build_tree(rightchild)
            leftchild = tree[leftchild]
            rightchild = tree[rightchild]

            quads = [leftchild.quads[0] + rightchild.quads[0],
                     leftchild.quads[1] + rightchild.quads[1],
                     leftchild.quads[2] + rightchild.quads[2],
                     leftchild.quads[3] + rightchild.quads[3]]
            tree[i] = Segment(leftchild.init, rightchild.end, quads)
        else:
            try:
                point = points[i - zero]
            except IndexError:
                point = Segment(i - zero + 1, i - zero + 1, [0,0,0,0])
            tree[i] = point

    _build_tree(1)
    return tree

def unit_swapping(node, previous, next):
    old = node.quads[previous]
    node.quads[previous] = node.quads[next]
    node.quads[next] = old

def update_tree(tree, query):

    def _update_tree(i, query):
        node = tree[i]
        if query.init > node.end or node.init > query.end:
            return
        if i < zero:
            _update_tree(i * 2, query)
            _update_tree(i * 2 + 1, query)
            leftchild = tree[i*2]
            rightchild = tree[i*2 + 1]
            node.quads = [leftchild.quads[0] + rightchild.quads[0],
                     leftchild.quads[1] + rightchild.quads[1],
                     leftchild.quads[2] + rightchild.quads[2],
                     leftchild.quads[3] + rightchild.quads[3]]

        elif query.tx:
            unit_swapping(node, QUAD_1, QUAD_4)
            unit_swapping(node, QUAD_2, QUAD_3)

        else:
            unit_swapping(node, QUAD_1, QUAD_2)
            unit_swapping(node, QUAD_4, QUAD_3)

    _update_tree(1, query)


def query_tree(tree, query):

    def _query_tree(i, query):
        node = tree[i]

        if query.init > node.end or node.init > query.end:
            return [0, 0, 0, 0]

        if node.init >= query.init and query.end >= node.end:
            return node.quads

        if i < zero:
            leftquads = _query_tree(i * 2, query)
            rightquads = _query_tree(i * 2 + 1, query)
            quads = [leftquads[0] + rightquads[0],
                     leftquads[1] + rightquads[1],
                     leftquads[2] + rightquads[2],
                     leftquads[3] + rightquads[3]]
            return quads

        elif query.tx:
            unit_swapping(node, QUAD_1, QUAD_4)
            unit_swapping(node, QUAD_2, QUAD_3)
            return node.quads
            
        else:
            unit_swapping(node, QUAD_1, QUAD_2)
            unit_swapping(node, QUAD_4, QUAD_3)
            return node.quads

    return _query_tree(1, query)


def main():

    import sys
    lines = sys.stdin.readlines()
    #lines = open('sample.txt').readlines()

    # get the points
    n_points = int(lines.pop(0))

    points = []
    for i in range(1, n_points + 1):
        coords = lines.pop(0).split()
        quads = [0] * 4
        quads[get_interval_from_coords(int(coords[0]), int(coords[1]))] = 1
        points.append(Segment(i, i, quads))
    tree = build_tree(points)

    n_queries = int(lines.pop(0))
    first = True
    for _ in range(n_queries):
        values = lines.pop(0).split()
        if values[0] == "X":
            query = Query(int(values[1]), int(values[2]), 1, 0)
            update_tree(tree, query)

        elif values[0] == "Y":
            query = Query(int(values[1]), int(values[2]), 0, 1)
            update_tree(tree, query)

        if values[0] == "C":
            query = Query(int(values[1]), int(values[2]), 0, 0)
            if not first:
                sys.stdout.write('\n')
            first = False
            quads = query_tree(tree, query)
            sys.stdout.write("{0} {1} {2} {3}".format(*quads))



if __name__ == '__main__':
    main()
