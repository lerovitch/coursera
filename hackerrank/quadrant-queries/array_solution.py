import sys
import itertools
from itertools import count
QUAD_3 = 3
QUAD_4 = 4
QUAD_2 = 2
QUAD_1 = 1

BEGIN = 0
END = 1

#Y = lambda x: (~x & 1) | (x & 2)
#X = lambda x: (~x & 3)
X = 0
Y = 1

def solve_x(points, i):
    if points[i] == QUAD_1:
        points[i] = QUAD_4
    elif points[i] == QUAD_2:
        points[i] = QUAD_3
    elif points[i] == QUAD_3:
        points[i] = QUAD_2
    elif points[i] == QUAD_4:
        points[i] = QUAD_1

def solve_y(points, i):
    if points[i] == QUAD_1:
        points[i] = QUAD_2
    elif points[i] == QUAD_2:
        points[i] = QUAD_1
    elif points[i] == QUAD_3:
        points[i] = QUAD_4
    elif points[i] == QUAD_4:
        points[i] = QUAD_3

def solve_c(points, i, j):
    count_q1 = 0
    count_q2 = 0
    count_q3 = 0
    count_q4 = 0
    for i in range(i, j+1):
        if points[i] == QUAD_1:
            count_q1 += 1
        elif points[i] == QUAD_2:
            count_q2 += 1
        elif points[i] == QUAD_3:
            count_q3 += 1
        elif points[i] == QUAD_4:
            count_q4 += 1

    sys.stdout.write("{0} {1} {2} {3}".format(count_q1, count_q2, count_q3, count_q4))

def process_points(points, i_points):
    i_points.sort(key=lambda x: x[0])
    first = i_points.pop(0)
    processing = [first]
    for i in count(first[0]):
        while i_points and i == i_points[0][0]:
            next = i_points.pop(0)
            if next[1] == END:
                processing = [x for x in processing if x[3] != next[3]]
            else:
                processing.append(next)
                processing.sort(key=lambda x: x[3])
        if not i_points:
            break
        for x in processing:
            if x[2] == 'X':
                solve_x(points, i)
            else:
                solve_y(points, i)

def main():
    import sys
    import time
    start_time = time.time()
    lines = sys.stdin.readlines()
    #lines = open("input03.txt").readlines()
    n_points = int(lines.pop(0))
    points = [None] * (n_points + 1)

    for i in range(1, n_points + 1):
        point = [int(x) for x in lines.pop(0).split()]
        if point[0] < 0:
            if point[1] < 0:
                points[i] = QUAD_3
            else:
                points[i] = QUAD_2
        else:
            if point[1] < 0:
                points[i] = QUAD_4
            else:
                points[i] = QUAD_1

    n_queries = int(lines.pop(0))
    queries = []
    first = True
    i_points = []
    for i in range(n_queries):
        query = lines.pop(0).split()
        query[1] = int(query[1])
        query[2] = int(query[2])
        if query[0] != "C":
            i_points.append((query[1], BEGIN, query[0], i))
            i_points.append((query[2] + 1, END, query[0], i))
        else:
            if not first:
                sys.stdout.write('\n')
            first = False
            if i_points:
                process_points(points, i_points)
            solve_c(points, query[1], query[2])
    end_time = time.time()
    sys.stderr.write("{0}".format(end_time - start_time))


if __name__ == '__main__':
    main()
    
    
