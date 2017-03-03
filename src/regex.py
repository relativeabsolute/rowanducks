# Author: Matt Gimbut
import re
import os


sample_file = "CMS2YSample.txt"
sample_HL_file = "CMS-2_HighLevel_2.txt"
valid_name = False

# Accepts 'X' followed by any number of digits or 'A/' followed by any number of digits.
exec_pattern = '(X[0-9]+|A/[0-9]+)'

# Accepts anything that ends in $
HL_statement_pattern ='(.*\$)'

# Accepts a '.' followed by any number of any characters until line ends to extract in-line comment.
single_comment_pattern = '(\. .*)'

# Accepts any digits followed by any number of white spaces, followed by 'COMMENT', followed by any characters.
block_comment_pattern = '([0-9]*\sCOMMENT.*)'

# Accepts two single apostrophes (''), followed by any characters/digits, followed by two single apostrophes.
note_pattern = '(\'\'[\w|\s|-]*\'\')'


def main():
    split_file(sample_HL_file)


# The method splits a CMS-2Y file by newline characters and prints out each line.
# This is just for testing and getting reacquainted with Python.
def split_file(file):
    f = open(file).read().splitlines()
    # for line in f:
    # print(line)
    analyze(f, sample_file)


# Analyzes given text
# Currently it only counts the number of executable lines and in line comments.
# Prints out findings when complete
def analyze(lines, name):
    # Before all else, check to see if valid file extension
    check_file_extension(name)

    goto_counter = 0

    block_comment_counter = 0
    block_comment_line_counter = 0
    block_comment_dictionary = {}

    note_counter = 0
    note_dictionary = {}

    HL_multi_statement_counter = 0
    HL_multi_statement_lines = 0
    HL_statement_counter = 0


    # Changed the "for in" loop to while so we can change loop counter when needed (see lines 100, 115)
    i = 0
    while (i < len(lines)):
        current_line = ""
        comment_text = ""
        statement_text = ""

        # Detects Direct CMS-2 code blocks and sends the entire block to be analyzed.
        if re.search('(DIRECT\s*\$)', lines[i]):
            for j in range(i, len(lines)):
                print(lines[j])
                if re.search("(CMS-2\s*\$)", lines[j]):
                    analyze_direct(lines[i:j+1])
                    break
        # This else handles all high-level code.
        else:
            current_line = re.match('(.*\s[0-9]+)', lines[i]).group(1)

            if 'GOTO' in lines[i]:
                # I'm not sure how to handle this yet, but the sample output keeps track of them.
                goto_counter += 1
                print("GOTO detected on line " + str(current_line))

            # Checks to see if the current line contains a programmer's note.
            if re.search(note_pattern, lines[i]):
                note_counter += 1
                # Adds note to note_dictionary.
                comment_text = re.search(note_pattern, lines[i]).group(1)
                note_dictionary[current_line] = comment_text

            # Checks first to see if a block comment is present. If not, checks for single line comments.
            # Using re.IGNORECASE because some comments are in lowercase in the sample
            elif re.search(block_comment_pattern, lines[i], re.IGNORECASE):
                block_comment_counter += 1
                # It loops through next lines until '$' is found (end of the comment).
                # Then it appends the message each iteration.
                for j in range(i, len(lines)):
                    block_comment_line_counter += 1
                    # TODO Maybe find a way to trim out tabs/repeating line numbers from message?
                    comment_text += lines[j]
                    block_comment_dictionary[i] = comment_text
                    if "$" in lines[j]:
                        # We should update loop counter so we don't double count
                        i = j
                        break

            # Check if it's a single liner
            elif re.search(HL_statement_pattern, lines[i]):
                HL_statement_counter += 1
            # If statement is not a note or comment or single liner it should be a multi line statement
            # Regex just to make sure the line has some information
            elif re.search('(.*\s[0-9]+)', lines[i]):
                # Not sure what information we want to record about these multi line statements
                HL_multi_statement_counter += 1
                for j in range(i, len(lines)):
                    HL_multi_statement_lines += 1
                    if "$" in lines[j]:
                        # Update counter to prevent double counting
                        i = j
                        break
            # Loop counter
            i+=1

    print
    print("Notes: " + str(note_counter))
    print
    print("Block comments: " + str(block_comment_counter))
    print("Block comment lines: " + str(block_comment_line_counter))
    print("Single line statements of High Level CMS: " + str(HL_statement_counter))
    print("Multi-line statements of High Level CMS: " + str(HL_multi_statement_counter))
    print("Lines of multi-line statements: " + str(HL_multi_statement_lines))
    print
    print("Total lines: " + str(len(lines)))
    print
    print

    # Prints all notes.
    for key, value in note_dictionary.items():
        print("Line " + key + " contains the note: " + value)

    # Prints all block comments
    print
    print("Block comments: ")
    for key, value in block_comment_dictionary.items():
        print(str(key) + ": " + value)


def check_file_extension(filename):
    file_, extension = os.path.splitext(filename)
    if extension.lower() == '.cts' or extension.lower() == '.cs2':
        valid_name = True
    else:
        valid_name = False
        print("Expected file extension .cts or .cs2, found " + extension + " in " + filename)


def analyze_direct(lines):
    single_comments_counter = 0
    single_comment_dictionary = {}
    executable_counter = 0

    for i in range(len(lines)):
        current_line = re.match(exec_pattern, lines[i]).group(1)

        # Checks to see if the current line is executable code.
        if re.match(exec_pattern, lines[i]):
            executable_counter += 1
            current_line = re.match(exec_pattern, lines[i]).group(1)

        # Checks to see if the current line contains an in-line comment.
        if re.search(single_comment_pattern, lines[i]):
            single_comments_counter += 1

            # Adds comment to single_comment_dictionary
            comment_text = re.search(single_comment_pattern, lines[i]).group(1)
            single_comment_dictionary[current_line] = comment_text

    print("Executable lines of Direct CMS2: " + str(executable_counter))
    print
    print("Single line comments: " + str(single_comments_counter))
    print
    # Prints all single line comments.
    for key, value in single_comment_dictionary.items():
        print("Line " + key + " contains the single line comment: " + value)


# TODO everything
def compare_files(original, modified):
    return


if __name__ == '__main__':
    main()
