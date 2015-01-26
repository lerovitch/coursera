"""
This script will compute get the median for a sequence of numbers of an array. It will return the number of its sum
in module 10000
"""
import argparse
from heapq import heappush, heappop, heapreplace

module_return = 10000


def parse_file(file_to_parse):
    with open(file_to_parse, 'r') as f:
        data = f.readlines()
        return [int(x.split('\n')[0]) for x in data]


def get_sum_of_medians(number_seq, module):
    result_sum = 0
    heap_low = []
    heap_high = []
    # Compute first element
    result_sum += number_seq[0]
    heappush(heap_low, -number_seq[0])
    # Compute second element
    result_sum += min(number_seq[0], number_seq[1])
    if number_seq[1] > number_seq[0]:
        heappush(heap_high, number_seq[1])
    else:
        heapreplace(heap_low, -number_seq[1])
        heappush(heap_high, number_seq[0])
    for x in range(2, len(number_seq)):
        high_minimum = -heap_low[0]
        low_maximum = heap_high[0]
        target_num = number_seq[x]
        if len(heap_high) == len(heap_low):
            if high_minimum >= target_num:
                heappush(heap_low, -target_num)
            else:
                if low_maximum >= target_num:
                    heappush(heap_low, -target_num)
                else:
                    elem = heappop(heap_high)
                    heappush(heap_low, -elem)
                    heappush(heap_high, target_num)
        elif len(heap_low) == len(heap_high) + 1:
            if low_maximum >= target_num:
                if high_minimum <= target_num:
                    heappush(heap_high, target_num)
                else:
                    elem = -heappop(heap_low)
                    heappush(heap_high, elem)
                    heappush(heap_low, -target_num)
            else:
                heappush(heap_high, target_num)
        result_sum = result_sum - heap_low[0]
    return result_sum % module


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a file with a number per line')
    parser.add_argument('--f', dest='file_to_parse',
        help='File to parse')

    args = parser.parse_args()

    numbers_seq = parse_file(args.file_to_parse)
    result = get_sum_of_medians(numbers_seq, module_return)
    print(result)
