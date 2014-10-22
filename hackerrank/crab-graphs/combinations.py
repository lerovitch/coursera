
def get_combinations(ls, number):
    elements = list(ls)
    result = list()
    for i, element in enumerate(elements):
        if number == 1:
            result.append([element])
        else:
            for rt in get_combinations(elements[i+1:], number - 1):
                rt.append(element)
                result.append(rt)
    return result


if __name__ == "__main__":
    result = get_combinations(range(5), 3)
    print result
