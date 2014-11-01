

from math import log


k = 0b11111111

def radix_sort(numbers, i):
    buckets = []
    for _ in range(k + 1):
        buckets.append([])

    for l in numbers:
        for j in l:
            i_byte = (j & ( k << 8 * i)) >> 8 * i
            buckets[i_byte].append(j)

    return buckets


def main():
    import sys
    numbers = [[int(x) for x in sys.stdin.readlines()]]

    passes = 4  # ordering 4 byte integers

    for i in range(passes):
        numbers = radix_sort(numbers, i)

    val = [] 
    for el in numbers:
        val.extend(el)
    print len(val)





if __name__ == '__main__':
    main()
