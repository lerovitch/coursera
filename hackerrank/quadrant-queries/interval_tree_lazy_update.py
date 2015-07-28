import sys
import itertools
import math
from collections import namedtuple
QUAD_1 = 0
QUAD_2 = 1
QUAD_3 = 2
QUAD_4 = 3

#Y = lambda x: (~x & 1) | (x & 2)
#X = lambda x: (~x & 3)
X = 0
Y = 1
BEGIN = 0
END = 1

DEBUG = False


def log(*args):
    if DEBUG:
        print args

def printa(*args):
    print args


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
            log('counting', i, i.query)
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
            log('pushing updating node in query', node)
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

        interval = Query(max(node.init, query.init), min(node.end, query.end))
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
            log('updating segment node', segment, segment.query)
            segment.op(tx, ty)
            # lazy evaluation
            if leftchild.query is not None:
                leftchild.query.tx += tx
                leftchild.query.ty += ty
            else:
                leftchild_query = Query(leftchild.init, leftchild.end)
                leftchild_query.tx = tx
                leftchild_query.ty = ty
                leftchild.query = leftchild_query
                log('leftchild query', leftchild, leftchild_query)
            if rightchild is not None:
                if rightchild.query is not None:
                    rightchild.query.tx += tx
                    rightchild.query.ty += ty
                else:
                    rightchild_query = Query(rightchild.init, rightchild.end)
                    rightchild_query.tx = tx
                    rightchild_query.ty = ty
                    rightchild.query = rightchild_query
                    log('rightchild query', rightchild, rightchild_query)
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

        log('propagating segment node', segment, leftchild, rightchild, query)
        if leftchild.query:
            lquery = leftchild.query
            leftchild.query = None
            self.update_node(leftchild, lquery)
        if rightchild and rightchild.query:
            rquery = rightchild.query
            rightchild.query = None
            self.update_node(rightchild, rquery)

        if leftchild.init <= query.init <= leftchild.end:
            left_query = Query(max(query.init, leftchild.init), min(query.end, leftchild.end))
            left_query.tx = query.tx
            left_query.ty = query.ty
            self.update_node(leftchild, left_query)
        if rightchild:
            if rightchild.init <= query.end <= rightchild.end:
                right_query = Query(max(query.init, rightchild.init), min(query.end, rightchild.end))
                right_query.tx = query.tx
                right_query.ty = query.ty
                self.update_node(rightchild,  right_query)

            for i in range(4):
                segment.quads[i] = leftchild.quads[i] + rightchild.quads[i]
            log('quads children update', segment, leftchild, rightchild)
        else:
            for i in range(4):
                segment.quads[i] = leftchild.quads[i]
            log('quads children update', segment, leftchild, rightchild)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.elements)


class Query(object):

    def __init__(self, init, end, qtype=None):
        self.init = init
        self.end = end
        self.tx = 1 if qtype == 'X' else 0
        self.ty = 1 if qtype == 'Y' else 0
        self.tc = 1 if qtype == 'C' else 0

    def __str__(self):
        return "Q {0} {1} tx:{2} ty:{3}".format(self.init, self.end, self.tx, self.ty)
    def __repr__(self):
        return self.__str__()


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


#@profile
def merge_queries(intervals):
    """
    integrate the interval C and return processed_interval and non_processed_intervals
    if an interval does not have C or tx % 2 != 0 or ty % 2 != 0, dismiss it
    """
    series = []
    for i in intervals:
        series.append((i.init, False, i.tx, i.ty, i.tc))
        series.append((i.end, True, i.tx, i.ty, i.tc))

    series.sort()

    processing_intervals = []
    skipped_intervals = []
    deleted_intervals = []

    first_series = series.pop(0)
    next_i = first_series[0]
    next_tx = first_series[2]
    next_ty = first_series[3]
    next_tc = first_series[4]

    for s in series:
        next_interval = None
        if s[1]:
            if next_i <= s[0]:
                next_interval = Query(next_i, s[0])
                next_interval.tx = next_tx
                next_interval.ty = next_ty
                next_interval.tc = next_tc
            next_i = s[0] + 1
            next_tx -= s[2]
            next_ty -= s[3]
            next_tc -= s[4]
        else:
            if next_i != s[0]:
                next_interval = Query(next_i, s[0] - 1)
                next_interval.tx = next_tx
                next_interval.ty = next_ty
                next_interval.tc = next_tc
                next_i = s[0]
            next_tx += s[2]
            next_ty += s[3]
            next_tc += s[4]

        if next_interval:
            if next_interval.tx % 2 == 0 and next_interval.ty % 2 == 0:
                deleted_intervals.append(next_interval)
                continue
            if next_interval.tc != 0:
                processing_intervals.append(next_interval)
            else:
                skipped_intervals.append(next_interval)

    return processing_intervals, skipped_intervals


def process_points(points, intervals):
    for i in intervals:
        if i.tx % 2:
            for j in range(i.i, i.j + 1):
                points.get(j).y = -points.get(j).y

        if i.ty % 2:
            for j in range(i.i, i.j + 1):
                points.get(j).x = -points.get(j).x


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
        query = Query(int(values[1]), int(values[2]), values[0])
        queries.append(query)
        if values[0] == "C":
            if not first:
                sys.stdout.write('\n')
            first = False
            #for q in queries:
            #    tree.update(1, q)
            #queries = []
            if queries:
                processing_queries, queries = merge_queries(queries)
                for q in processing_queries:
                    tree.update(1, q)
            tree.query(query)


if __name__ == '__main__':
    main()
    
    
