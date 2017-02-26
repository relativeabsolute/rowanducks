# Author: Matt Gimbut
import re
import os


sample_file = "CMS2YSample.txt"
valid_name = False


def main():
    split_file(sample_file)


# Splits a CMS-2Y file by newline characters and prints out each line.
# This is just for testing right now and getting reacquainted with Python.
def split_file(file):
    f = open(file).read().splitlines()
    # for line in f:
    # print(line)
    analyze(f, sample_file)


# Analyzes given text.
# As of now, only counts the number of executable lines and in line comments.
# Prints out findings when complete.
def analyze(lines, name):
    # Before all else, check to see if valid file extension
    check_file_extension(name)

    single_comments_counter = 0
    single_comment_dictionary = {}

    executable_counter = 0
    goto_counter = 0

    block_comment_counter = 0
    block_comment_line_counter = 0
    block_comment_dictionary = {}

    note_counter = 0
    note_dictionary = {}

    # Accepts 'X' followed by any number of digits or 'A/' followed by any number of digits.
    exec_pattern = '(X[0-9]+|A/[0-9]+)'

    # Accepts a '.' followed by any number of any characters until line ends to extract in-line comment.
    single_comment_pattern = '(\. .*)'

    # Accepts any digits followed by any number of white spaces, followed by 'COMMENT', followed by any characters.
    block_comment_pattern = '([0-9]*\sCOMMENT.*)'

    # Accepts two single apostrophes (''), followed by any characters/digits, followed by two single apostrophes.
    note_pattern = '(''[\w|\s]*'')'      #'([\w|\s]* '' [\w|\s]* '')|(''[\w|\s]*'')'

    for i in range(len(lines)):
        current_line = ""
        comment_text = ""

        # Checks to see if the current line is executable code.
        if re.match(exec_pattern, lines[i]):
            executable_counter += 1
            current_line = re.match(exec_pattern, lines[i]).group(1)

        # Checks to see if the current line contains a programmer's note.
        if re.search(note_pattern, lines[i]):
            note_counter += 1
            # Adds note to note_dictionary.
            comment_text = re.search(note_pattern, lines[i]).group(1)
            note_dictionary[current_line] = comment_text

        # Checks first to see if a block comment is present. If not, checks for single line comments.r
        if re.search(block_comment_pattern, lines[i]):
            block_comment_counter += 1
            j = 0
            # Loops through next lines until '$' is found (end of the comment). Appends to message each iteration.
            for j in range(i, len(lines)):
                block_comment_line_counter += 1
                # TODO Maybe find a way to trim out tabs/repeating line numbers from message?
                comment_text += lines[j]
                if "$" in lines[j]:
                    break
            block_comment_dictionary[i] = comment_text

        # Checks to see if the current line contains an in-line comment.
        elif re.search(single_comment_pattern, lines[i]):
            single_comments_counter += 1

            # Adds comment to single_comment_dictionary.
            comment_text = re.search(single_comment_pattern, lines[i]).group(1)
            single_comment_dictionary[current_line] = comment_text

        if 'GOTO' in lines[i]:
            # Not sure how to handle this yet, but the sample output keeps track of them.
            goto_counter += 1
            print("GOTO detected on line " + str(current_line))

    print()
    print("Notes: " + str(note_counter))
    print()
    print("Single line comments: " + str(single_comments_counter))
    print()
    print("Block comments: " + str(block_comment_counter))
    print("Block comment lines: " + str(block_comment_line_counter))
    print("Executable lines of code: " + str(executable_counter))
    print("Total lines: " + str(len(lines)))
    print()
    print()

    # Prints all notes.
    for key, value in note_dictionary.items():
        print("Line " + key + " contains the note: " + value)

    # Prints all single line comments.
    for key, value in single_comment_dictionary.items():
        print("Line " + key + " contains the single line comment: " + value)

    # Prints all block comments.
    print()
    print("Block comments: ")
    for key, value in block_comment_dictionary.items():
        print(str(key) + ": " + value)


def check_file_extension(filename):
    file, extension = os.path.splitext(filename)
    if extension.lower() == '.cts' or extension.lower() == '.cs2':
        valid_name = True
    else:
        valid_name = False
        print("Expected file extension .cts or .cs2, found " + extension)


# TODO everything
def compare_files(original, modified):
    return


if __name__ == '__main__':
    main()
