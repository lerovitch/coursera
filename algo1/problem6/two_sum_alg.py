"""
This script will compute the number of sums between interval [-10000, 10000] that are fulfilled by the addition of
two numbers in the text file
"""
import argparse

max_limit = 10000
min_limit = -10000


def parse_file(file_to_parse):
    with open(file_to_parse, 'r') as f:
        data = f.readlines()
        numbers = set([])
        for x in data:
            numbers.add(int(x.split('\n')[0]))
        return numbers

def get_two_sum(numbers_seq, maximum, minimum):
    numbers_dict = dict((x, True) for x in numbers_seq)
    number_of_sums = 0
    sorted_list = list(numbers_seq)
    sorted_list.sort()

    for t in range(minimum, maximum + 1):
        if t%100 ==0:
            print "Evaulating {0}".format(t)
        max_to_check = t/2 + 1
        for number in sorted_list:
            if number > max_to_check:
                break
            search_value = t - number
            if numbers_dict.get(search_value) and search_value != number:
                number_of_sums += 1
                print "Provisional sums is {0} at sum {1}".format(number_of_sums, t)
                break
    return number_of_sums


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a file with a number per line')
    parser.add_argument('--f', dest='file_to_parse',
        help='File to parse')

    args = parser.parse_args()

    numbers_seq = parse_file(args.file_to_parse)
    result = get_two_sum(numbers_seq, max_limit, min_limit)
    print(result)
