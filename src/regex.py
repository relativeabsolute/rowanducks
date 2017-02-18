# Author: Matt Gimbut
import re


def main():
    split_file("CMS2YSample.txt")


# Splits a CMS-2Y file by newline characters and prints out each line.
# This is just for testing right now and getting reacquainted with Python.
def split_file(file):
    f = open(file).read().splitlines()
    # for line in f:
    # print(line)
    analyze(f)


# Analyzes given text.
# As of now, only counts the number of executable lines and in line comments.
# Prints out findings when complete.
def analyze(lines):
    comments = 0
    executable = 0
    comment_dictionary = {}

    # Accepts 'X' followed by any number of digits or 'A/' followed by any number of digits.
    exec_pattern = '(X[0-9]+|A/[0-9]+)'

    # Accepts a '.' followed by any number of any characters until line ends to extract in-line comment.
    single_comment_pattern = '(\. .*)'

    for line in lines:
        current_line = ""
        comment_text = ""

        # Checks to see if the current line is executable code.
        if re.match(exec_pattern, line):
            executable += 1
            current_line = re.match(exec_pattern, line).group(1)

        # Checks to see if the current line contains an in-line comment.
        if re.search(single_comment_pattern, line):
            comments += 1

            # Adds comment to comment_dictionary.
            comment_text = re.search(single_comment_pattern, line).group(1)
            comment_dictionary[current_line] = comment_text

    print()
    print("Single line comments: " + str(comments))
    print("Executable lines of code: " + str(executable))
    print("Total lines: " + str(len(lines)))
    print()
    print()
    for key, value in comment_dictionary.items():
        print("Line " + key + " contains the comment: " + value)


# TODO everything
def compare_files(original, modified):
    return


if __name__ == '__main__':
    main()
