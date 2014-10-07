import sys


def main():
    data = sys.stdin.readlines()
    for line in data:
        print line[:-1]  # removing newline from read line


if __name__ == "__main__":
    main()

