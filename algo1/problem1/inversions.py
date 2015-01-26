#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


def merge(left_ls, right_ls):
    l_len = len(left_ls)
    r_len = len(right_ls)
    t_len = l_len + r_len
    result_ls = []

    i = 0  # iterate over left
    j = 0  # iterate over right
    k = 0  # keep track of elements in results
    inv = 0  # keep track of inversions

    while i < l_len or j < r_len:
        if i == l_len:
            # left is exhausted
            result_ls.append(right_ls[j])
            j += 1
        elif j == r_len:
            # right is exhausted
            result_ls.append(left_ls[i])
            i += 1
        else:
            if left_ls[i] <= right_ls[j]:
                result_ls.append(left_ls[i])
                i += 1
            else:
                result_ls.append(right_ls[j])
                inv += (l_len - i)
                j += 1
        k += 1

    return result_ls, inv


def sort(int_ls):
    '''return a sorted list of int_ls
    '''
    inv = 0
    lenght = len(int_ls)

    if lenght > 1:
        left_ls, left_inv = sort(int_ls[:lenght/2])
        right_ls, right_inv = sort(int_ls[lenght/2:])
        merged_ls, merged_inv = merge(left_ls, right_ls)
        inv = left_inv + right_inv + merged_inv
    
    else:
        merged_ls = int_ls

    return merged_ls, inv


def main():
    input_ls = [int(x.strip()) for x in sys.stdin.readlines()]
    print sort(input_ls)[1]



if __name__ == '__main__':
    main()
