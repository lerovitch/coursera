import sys

R = 10


def msd_sort(o_numbers, i_init, i_fin, i):
    """
        :param o_numbers: array of numbers
        :param i_init: first element
        :param i_fin: last element
        :param i: index element to revisit

    """
    numbers = [o_numbers[j] for j in range(i_init, i_fin + 1)]

    count = [0] * (R + 1)

    # creating the key count array
    for item in numbers:
        try:
            index = int(item[i]) 
        except IndexError:
            index = 0
        count[index + 2] += 1

    # reassigning positions of the values
    for j in range(R + 1):
        count[j+1] += count[j]

    for item in numbers:
        try:
            index = int(item[i]) 
        except IndexError:
            index = 0

        o_numbers[i_init + count[index]] = item
        count[index] += 1

    msd_sort(o_numbers, 




def main():
    """ first implementation sorting knowing that the max lenght is 5
    """

    import sys
    numbers = [x.strip() for x in sys.stdin.readlines()]

    numbers = lsd_sort(numbers, k=5)


if __name__ == '__main__':
    main()    
