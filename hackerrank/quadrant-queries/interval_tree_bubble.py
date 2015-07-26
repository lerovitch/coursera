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


class Tree(object):

    def __init__(self, n):
        level = int(math.ceil(math.log(n, 2)))
        self.elements = [None] * (2 ** (level + 1))
        self.i = 2 ** level
        self.zero = 2 ** level

    def query(self, interval):
        quads = [0] * 4
        for i in self.get_nodes(1, interval):
            if isinstance(i, Point):
                print 'counting', i
                quads[i.interval] += 1
            else:
                print 'counting', i
                if i.n == 5:
                    pass
                for j in range(4):
                    quads[j] += i.quads[j]
        sys.stdout.write("{0} {1} {2} {3}".format(*quads))

    def get_nodes(self, i_node, interval):
        ret_nodes = []
        node = self.elements[i_node]
        if node is None:
            return
        interval = Interval(None, max(node.i, interval.i), min(node.j, interval.j))
        if node.i == interval.i and node.j == interval.j:
            ret_nodes.append(node)
        elif node.j < interval.i or interval.j < node.i:
            return
        else:  # there is some intersection
            left_nodes = self.get_nodes(i_node * 2, interval)
            if left_nodes:
                ret_nodes.extend(left_nodes)
            right_nodes = self.get_nodes(i_node * 2 + 1, interval)
            if right_nodes:
                ret_nodes.extend(right_nodes)
        return ret_nodes

    def build(self):
        for i in range(self.zero - 1, 0, -1):
            # get nodes 
            left_node = self.elements[2*i]
            right_node = self.elements[2*i + 1]

            # create new interval
            if isinstance(left_node, Point):
                if isinstance(right_node, Point):
                    interval = Interval(None, 2*i - self.zero + 1, (2*i + 1) - self.zero + 1)
                    interval.quads[right_node.interval] += 1
                else:
                    interval = Interval(None, 2*i - self.zero + 1, 2*i - self.zero + 1)
                interval.quads[left_node.interval] += 1
            elif isinstance(right_node, Interval):
                interval = Interval(None, left_node.i, right_node.j)
                for j in range(4):
                    interval.quads[j] = left_node.quads[j] + right_node.quads[j]
            elif isinstance(left_node, Interval):
                interval = Interval(None, left_node.i, left_node.j)
                for j in range(4):
                    interval.quads[j] = left_node.quads[j]
            else:
                continue
            interval.n = i
            self.elements[i] = interval

    def append(self, element):
        self.elements[self.i] = element
        element.i = element.j = self.i - self.zero + 1
        self.i += 1

    def get(self, index):
        return self.elements[self.zero + index - 1] 

    #@profile
    def update(self, interval):
        for i in range(interval.i, interval.j + 1):
            index = self.zero + i - 1
            op = self.elements[index].op(interval.tx, interval.ty)
            self._bubble_update(index / 2, op)

    #@profile
    def _bubble_update(self, parent_index, op):
        node = self.elements[parent_index]
        if node:
            node.quads[op[0]] -= 1
            node.quads[op[1]] += 1
            parent_index = parent_index / 2
            if parent_index != 0:
                self._bubble_update(parent_index, op)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.elements)


class Interval(object):

    def __init__(self, t, i, j):
        self.i = int(i)
        self.j = int(j)
        self.tx = 1 if t == 'X' else 0
        self.ty = 1 if t == 'Y' else 0
        self.tc = 1 if t == 'C' else 0
        self.quads = [0] * 4
        self.n = -1
            
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '{3} ({0}, {1}) {2} {4} {5} {6}'.format(self.i, self.j, self.quads, self.n, self.tx, self.ty, self.tc)


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.i = -1
        self.j = -1
        self.interval = self._get_interval() 

    def op(self, tx, ty):
        if tx % 2:
            self.y = -self.y
        if ty % 2:
            self.x = -self.x
        old_interval = self.interval
        self.interval = self._get_interval()
        return (old_interval, self.interval)

    def _get_interval(self):
        if self.x < 0:
            if self.y < 0:
                return QUAD_3
            else:
                return QUAD_2
        else:
            if self.y < 0:
                return QUAD_4
            else:
                return QUAD_1

    def __repr__(self):
        return 'P int {0}'.format(self.interval + 1)

#@profile
def merge_intervals(intervals):
    """
    integrate the interval C and return processed_interval and non_processed_intervals
    if an interval does not have C or tx % 2 != 0 or ty % 2 != 0, dismiss it
    """
    Serie = namedtuple('Serie', ['point', 'is_end', 'tx', 'ty', 'tc'])
    series = []
    for i in intervals:
        series.append(Serie(i.i, False, i.tx, i.ty, i.tc))
        series.append(Serie(i.j, True, i.tx, i.ty, i.tc))

    series.sort()

    processing_intervals = []
    skipped_intervals = []
    deleted_intervals = []

    first_series = series.pop(0)
    assert first_series[1] == BEGIN
    next_i = first_series[0]
    next_tx = first_series[2]
    next_ty = first_series[3]
    next_tc = first_series[4]

    for s in series:
        next_interval = None
        if s.is_end:
            if next_i <= s.point:
                next_interval = Interval(None, next_i, s.point)
                next_interval.tx = next_tx
                next_interval.ty = next_ty
                next_interval.tc = next_tc
            next_i = s.point + 1
            next_tx -= s.tx
            next_ty -= s.ty
            next_tc -= s.tc
        else:
            if next_i != s.point:
                next_interval = Interval(None, next_i, s.point - 1)
                next_interval.tx = next_tx
                next_interval.ty = next_ty
                next_interval.tc = next_tc
                next_i = s.point
            next_tx += s.tx
            next_ty += s.ty
            next_tc += s.tc

        if next_interval:
            if next_interval.tx % 2 == 0 and next_interval.ty % 2 == 0:
                deleted_intervals.append(next_interval)
                continue
            if next_interval.tc != 0:
                processing_intervals.append(next_interval)
            else:
                skipped_intervals.append(next_interval)

    #print 'intervals:', intervals
    #print 'processing:', processing_intervals
    #print 'skipped_intervals:', skipped_intervals
    #print 'deleted_intervals:', deleted_intervals

    return processing_intervals, skipped_intervals


def process_points(points, intervals):
    for i in intervals:
        if i.tx % 2:
            for j in range(i.i, i.j + 1):
                points.get(j).y = -points.get(j).y

        if i.ty % 2:
            for j in range(i.i, i.j + 1):
                points.get(j).x = -points.get(j).x

#@profile
def main():
    import sys
    #lines = sys.stdin.readlines()
    lines = open('input01.txt').readlines()

    # get the points
    n_points = int(lines.pop(0))
    tree = Tree(n_points)
    for i in range(1, n_points + 1):
        coords = lines.pop(0).split()
        tree.append(Point(int(coords[0]), int(coords[1])))

    tree.build()

    n_queries = int(lines.pop(0))
    queries = []
    first = True
    intervals = []
    #for _ in range(n_queries):
    for _ in range(45):
            values = lines.pop(0).split()
            intervals.append(Interval(*values))
            if values[0] == "C":

                if not first:
                    sys.stdout.write('\n')
                first = False
                if intervals:
                    processing_intervals, intervals = merge_intervals(intervals)
                    for interval in processing_intervals:
                        tree.update(interval)
                query_interval = Interval(None, int(values[1]), int(values[2]))
                print 'query_interval', query_interval
                tree.query(query_interval)


if __name__ == '__main__':
    main()
    
    
