import sys

R = 10


def lsd_sort(numbers, k):

    lenght = len(numbers)

    for i in range(1, k + 1):
        count = [0] * (R + 1)
        print i
        for item in numbers:
            try:
                index = int(item[-i]) 
            except IndexError:
                index = 0
            count[index + 2] += 1

        for j in range(R + 1):
            if j != 0:
                count[j] = count[j] + count[j-1]

        new_numbers = [None] * len(numbers)

        for item in numbers:
            try:
                index = int(item[-i]) 
            except IndexError:
                index = 0

            new_numbers[count[index]] = item
            count[index] += 1
    
        numbers = new_numbers

    return numbers


def main():
    """ first implementation sorting knowing that the max lenght is 5
    """

    import sys
    numbers = [x.strip() for x in sys.stdin.readlines()]

    numbers = lsd_sort(numbers, k=5)


if __name__ == '__main__':
    main()    
