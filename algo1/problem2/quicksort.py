#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


def swap(array, i, j):
    temp = array[i]
    array[i] = array[j]
    array[j] = temp

def get_pivot(array, i_init, i_end): 
    # case 1: pivot=0
    # case 2: pivot=i_end - 1
    # case 3: pivot= median
    i_end -= 1
    median = i_init + ((i_end - i_init) / 2)

    if array[i_init] < array[i_end]:
        if array[i_end] < array[median]:
            pivot = i_end
        elif array[median] < array[i_init]:
            pivot = i_init
        else:
            pivot = median
    else:
        if array[i_init] < array[median]:
            pivot = i_init
        elif array[median] < array[i_end]:
            pivot = i_end
        else:
            pivot = median
    pivot = pivot
    swap(array, i_init, pivot)


def qsort(array, i_init, i_end):
    # taking the first element as the pivot
    if i_end - i_init < 2:
        return 0
    comp = (i_end - i_init) - 1
    get_pivot(array, i_init, i_end)

    pivot = array[i_init]
    i_pivot = i_init
    i = i_init
    for j in range(i_init + 1, i_end): # i_end is not taken
        if array[j] < pivot:
            i += 1
            swap(array, i, j)
        j += 1
    swap(array, i_pivot, i)
    
    comp += qsort(array, i_init, i)
    comp += qsort(array, i + 1, i_end)
    return comp


def main():
    numbers = [int(x.strip()) for x in sys.stdin.readlines()]
    #numbers = [int(x.strip()) for x in open("qsort.txt").readlines()]
    comp = qsort(numbers, 0, len(numbers))
    print comp


    



if __name__ == '__main__':
    main()
