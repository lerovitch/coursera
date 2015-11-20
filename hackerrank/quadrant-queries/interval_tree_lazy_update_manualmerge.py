import sys
import itertools
import math
from collections import namedtuple
from interval import update, Query, intersect_update
QUAD_1 = 0
QUAD_2 = 1
QUAD_3 = 2
QUAD_4 = 3

X = 0
Y = 1
BEGIN = 0
END = 1

class SegmentTree(object):

    def __init__(self, n):
        level = int(math.ceil(math.log(n, 2)))
        self.elements = [None] * (2 ** (level + 1))
        self.i = 2 ** level
        self.zero = 2 ** level
    
    def append(self, element):
        self.elements[self.i] = element
        self.n = self.i - self.zero + 1
        element.init = element.end = self.n
        element.n = self.i
        self.i += 1

    def get(self, index):
        return self.elements[self.zero + index - 1] 

    #@profile
    def query(self, query):
        quads = [0] * 4
        for i in self.get_nodes(1, query):
            for j in range(4):
                quads[j] += i.quads[j]
        sys.stdout.write("{0} {1} {2} {3}".format(*quads))

    #@profile
    def get_nodes(self, i_node, query):
        ret_nodes = []
        node = self.elements[i_node]
        if node is None:
            return
        if node.query is not None:
            if node.init != node.end:
                leftnode = self.elements[node.n * 2]
                rightnode = self.elements[node.n * 2 + 1]

                q = node.query
                node.query = None
                self._update_segment(node, leftnode, rightnode,
                                     q.tx, q.ty) 
            else:
                qnode = node.query
                node.query = None
                node.op(qnode.tx, qnode.ty)

        interval = Query(max(node.init, query.init), min(node.end, query.end), None, None)
        if node.init == interval.init and node.end == interval.end:
            ret_nodes.append(node)
        elif node.end < interval.init or interval.end < node.init:
            return
        else:  # there is some intersection
            left_nodes = self.get_nodes(i_node * 2, interval)
            if left_nodes:
                ret_nodes.extend(left_nodes)
            right_nodes = self.get_nodes(i_node * 2 + 1, interval)
            if right_nodes:
                ret_nodes.extend(right_nodes)
        return ret_nodes

    #@profile
    def build(self):
        for i in range(self.zero - 1, 0, -1):
            # get nodes 
            left_node = self.elements[2*i]
            # create new interval
            if left_node is None:
                continue
            right_node = self.elements[2*i + 1]

            if right_node is not None:
                segment = Segment(left_node.init, right_node.end, [0]*4)
                segment.update_quads(left_node, right_node)
            else:
                segment = Segment(left_node.init, left_node.end, [0]*4)
                segment.update_quads_left(left_node)

            segment.n = i
            self.elements[i] = segment

    def update(self, i_node, query):
        segment = self.elements[i_node]
        if segment is not None:
            self.update_node(segment, query)

    #@profile 
    def _update_segment(self, segment, leftchild, rightchild, tx, ty):

        # check it is a perfect match of segments
            segment.op(tx, ty)
            # lazy evaluation
            if leftchild.query is not None:
                leftchild.query.tx += tx
                leftchild.query.ty += ty
            else:
                leftchild_query = Query(leftchild.init, leftchild.end, tx, ty)
                leftchild.query = leftchild_query
            if rightchild is not None:
                if rightchild.query is not None:
                    rightchild.query.tx += tx
                    rightchild.query.ty += ty
                else:
                    rightchild_query = Query(rightchild.init, rightchild.end, tx, ty)
                    rightchild.query = rightchild_query
            return 

    #@profile
    def update_node(self, segment, query):

        if segment is None or segment.init > query.end or segment.end < query.init:
            return

        # check it is a leaf node, update it if yes 
        if segment.init == segment.end:
            tx = query.tx
            ty = query.ty
            segment.op(tx, ty)
            segment.query = None
            return 

        i_leftchild = 2*segment.n
        i_rightchild = 2*segment.n + 1
        leftchild = self.elements[i_leftchild]
        rightchild = self.elements[i_rightchild]

        if segment.init == query.init and segment.end == query.end:
            tx = query.tx
            ty = query.ty
            self._update_segment(segment, leftchild, rightchild, tx, ty)
            return

        # propagate update
        #if segment.query:
        #    self._update_segment(segment, leftchild, rightchild, segment.query.tx, segment.query.ty)

        if leftchild.query:
            lquery = leftchild.query
            leftchild.query = None
            self.update_node(leftchild, lquery)
        if rightchild and rightchild.query:
            rquery = rightchild.query
            rightchild.query = None
            self.update_node(rightchild, rquery)

        if leftchild.init <= query.init <= leftchild.end:
            left_query = Query(max(query.init, leftchild.init), min(query.end, leftchild.end), query.tx, query.ty)
            self.update_node(leftchild, left_query)
        if rightchild:
            if rightchild.init <= query.end <= rightchild.end:
                right_query = Query(max(query.init, rightchild.init), min(query.end, rightchild.end), query.tx, query.ty)
                self.update_node(rightchild,  right_query)

            for i in range(4):
                segment.quads[i] = leftchild.quads[i] + rightchild.quads[i]
        else:
            for i in range(4):
                segment.quads[i] = leftchild.quads[i]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.elements)


class Segment(object):

    def __init__(self, init, end, quads=None):
        self.init = int(init) if init else None
        self.end = int(end) if end else None
        self.quads = quads
        self.n = -1
        self.query = None

    #@profile
    def op(self, tx, ty):
        def _unit_swapping(previous, next):
            old = self.quads[previous]
            self.quads[previous] = self.quads[next]
            self.quads[next] = old

        if tx % 2 != 0:
            _unit_swapping(QUAD_1, QUAD_4)
            _unit_swapping(QUAD_2, QUAD_3)
        if ty % 2 != 0:
            _unit_swapping(QUAD_1, QUAD_2)
            _unit_swapping(QUAD_4, QUAD_3)

    def update_quads(self, left_node, right_node):
        for i in range(4):
            self.quads[i] = left_node.quads[i] + right_node.quads[i]

    def update_quads_left(self, left_node):
        self.quads = list(left_node.quads)
            
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


#@profile
def main():
    import sys
    lines = sys.stdin.readlines()

    # get the points
    n_points = int(lines.pop(0))
    tree = SegmentTree(n_points)
    for i in range(1, n_points + 1):
        coords = lines.pop(0).split()
        quads = [0] * 4
        quads[get_interval_from_coords(int(coords[0]), int(coords[1]))] = 1
        tree.append(Segment(None, None, quads))

    tree.build()

    n_queries = int(lines.pop(0))
    first = True
    queries = []
    for _ in range(n_queries):
        values = lines.pop(0).split()
        if values[0] == "X":
            query = Query(int(values[1]), int(values[2]), tx=1, ty=0)
            tree.update(1,query)
            #queries = update(query, queries)
        elif values[0] == "Y":
            query = Query(int(values[1]), int(values[2]), tx=0, ty=1)
            tree.update(1,query)
            #queries = update(query, queries)
        else:
            query = Query(int(values[1]), int(values[2]), None, None)
            #queries, updates = intersect_update(query, queries)

            if not first:
                sys.stdout.write('\n')
            first = False
            #for q in updates:
            #    tree.update(1, q)
            tree.query(query)


if __name__ == '__main__':
    main()
    
    
