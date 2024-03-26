from collections import Counter
import argparse

cash = {}


# main function

def lonely_characters_counter(some_string):
    if some_string in cash:
        return cash[some_string]
    else:
        counted_list = Counter(list(some_string))
        needed_value = 1
        sum_of_lonely_characters = sum(value for key, value in counted_list.items() if value == needed_value)
        cash.update({some_string: sum_of_lonely_characters})
        return sum_of_lonely_characters


def main():
    parser = argparse.ArgumentParser(description="Give a string or path to file with a string to proceed")
    parser.add_argument('--string', type=str, help="string to be counted")
    parser.add_argument('--file', type=open, help="open a file")
    args = parser.parse_args()
    if args.file is None:
        if args.string is None:
            print(0)
        else:
            print(lonely_characters_counter(args.string))
    else:
        with open(args.file, 'r') as file:
            file_content = file.read()
            print(lonely_characters_counter(file_content))


if __name__ == "__main__":
    main()
