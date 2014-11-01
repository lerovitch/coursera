

from math import log


k = 10

def get_passes(numbers):
    max_value = None

    for i in numbers:
        if max_value and i > max_value:
            max_value = i

    return 1 + int(log(i, k))


def radix_sort(numbers, i):
    buckets = []
    for _ in range(k):
        buckets.append([])

    for j in numbers:
        try:
            last_digit = str(j)[-(1+i)]
        except IndexError:
            last_digit = 0
        buckets[int(last_digit)].append(j)

    ret_bucket = [] 
    for el in buckets:
        ret_bucket.extend(el)

    return ret_bucket


def main():
    import sys
    numbers = [int(x) for x in sys.stdin.readlines()]

    passes = get_passes(numbers)

    for i in range(passes):
        numbers = radix_sort(numbers, i)
    print numbers





if __name__ == '__main__':
    main()
