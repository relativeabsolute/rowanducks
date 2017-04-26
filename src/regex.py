# Author: Matt Gimbut / Tom Harker / Chris Curreri

# README
# To run this program do one of the following:
# 1. Use command line tool and pass directory name (or filename(s)) as parameter
#       On a Mac open Terminal and navigate to this src folder. Type 'python regex.py SampleDirectory' hit enter
# 2. On top menu go to Run->Edit Configurations, and add SampleDirectory as a script parameter and hit Apply and OK

import re
import os
import sys
from collections import OrderedDict
from CMS2File import CMS2File

sample_file = "/SampleDirectory/CMS2YSample.txt"
sample_HL_file = "/SampleDirectory/CMS-2_HighLevel_2.txt"
valid_name = False

block_comments = 0
comment_lines = 0
instructions = 0

# Accepts 'X' followed by any number of digits or 'A/' followed by any number of digits.
exec_pattern = '(X[0-9]+|A/[0-9]+)'

# Accepts anything that ends in $
hl_statement_pattern = '(.*\$)'

# Accepts a '.' followed by any number of any characters until line ends to extract in-line comment.
single_comment_pattern = '(\. .*)'

# Accepts any digits followed by any number of white spaces, followed by 'COMMENT', followed by any characters.
block_comment_pattern = '([0-9]*\sCOMMENT.*)'

# Accepts any characters followed by 'SYS-PROC' followed by any characters and a '$'
direct_start_procedure_pattern = '(\.*SYS-PROC\s*\$)'

# Accepts any characters followed by 'END-SYS-PROC' followed by any characters and a '$'
direct_end_procedure_pattern = '(\.*END-SYS-PROC.*\$)'

# Accepts any characters followed by 'PROCEDURE' followed by any characters and a '$'
hl_start_procedure_pattern = '(\.*PROCEDURE.*\$)'

# Accepts any characters followed by 'RETURN' followed by any characters and a '$'
hl_end_procedure_pattern = '(\.*RETURN.*\$)'

# The three major types of data statements are switches, variables, and aggregates
data_statement_pattern = '((.*SET.*TO.*\$)|(.*SWITCH.*\$.*END-SWITCH.*\$)|(.*FIELD\b\S*\b.*\$))'

# Accepts two single apostrophes (''), followed by any characters/digits, followed by two single apostrophes.
note_pattern = '(\'\'[\w|\s|-]*\'\')'

# Accepts any white space, followed by any capital or lower case letters, more white space, and then SYS-PROC $.
direct_function_name_pattern = '(\s*[a-zA-Z]*\s*SYS-PROC\s*\$)'

# Accepts PROCEDURE followed by capital or lower case letters, then white space and '$'.
hl_function_name_pattern = '(PROCEDURE\s*[a-zA-Z]*\s\$)'


def main(arg_list):
    finished = False
    input_files = []
    list_cms2file = []

    # Takes arguments (filenames) from command line separated by spaces
    # Could update this to take a directory and analyze all files in directory
    for item in arg_list:
        if os.path.isfile(item):
            input_files.append(item)
        elif os.path.isdir(item):
            file_list = get_files_from_dir(item)
            for file_name in file_list:
                input_files.append(file_name)

    for location in input_files:
        list_cms2file.append(split_file(location))
    for file_data in list_cms2file:
        print (file_data.print_string())

    return list_cms2file


def get_files_from_dir(directory):
    file_paths = []  # List which will store all of the full file paths.

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.
    return file_paths


# The method splits a CMS-2Y file by newline characters and sends it to analyze().
# Returns the OrderedDict sent back by analyze().
def split_file(file):
    f = open(file).read().splitlines()
    # for line in f:
    # print(line)
    return analyze(f, file)

# Analyzes given text
# Currently it only counts the number of executable lines and in line comments.
# Returns findings in an OrderedDict on completion
def analyze(lines, name):
    global block_comments
    global comment_lines
    global instructions

    # Before all else, check to see if valid file extension
    check_file_extension(name)
    lines_length = len(lines)

    goto_counter = 0


    block_comment_counter = 0
    comment_line_counter = 0
    block_comment_dictionary = {}

    note_counter = 0
    note_dictionary = {}

    hl_multi_statement_counter = 0
    hl_multi_statement_lines = 0
    hl_statement_counter = 0

    hl_executable_counter = 0


    hl_data_statement_counter = 0
    procedure_over_250 = []
    procedure_230_250 = []

    # Changed the "for in" loop to while so we can change loop counter when needed (see lines 100, 115)
    i = 0
    file_info = OrderedDict()
    while i < lines_length:
        current_line = ""
        comment_text = ""
        statement_text = ""

        # Detects Direct CMS-2 code blocks and sends the entire block to be analyzed.
        if re.search('(DIRECT\s*\$)', lines[i]):
            for j in range(i, lines_length):
                if re.search("(CMS-2\s*\$)", lines[j+1]):
                    file_info.update(analyze_direct(lines[i:j], procedure_over_250, procedure_230_250))
                    i = j + 1  # Update loop counter so we don't analyze code block more than once
                    break
            i = j + 1  # Prevent infinite loop if code sample improperly formatted
        # This else handles all high-level code.
        else:
            if 'GOTO' in lines[i]:
                # I'm not sure how to handle this yet, but the sample output keeps track of them.
                goto_counter += 1
                # print("GOTO detected on line " + str(current_line))

            # Checks to see if the current line contains a programmer's note.
            if re.search(note_pattern, lines[i]):
                note_counter += 1
                # Adds note to note_dictionary.
                comment_text = re.search(note_pattern, lines[i]).group(1)
                note_dictionary[current_line] = comment_text

            # Checks to see if the current line contains an executable statement
            if re.search(exec_pattern, lines[i]):
                hl_executable_counter += 1

            # Checks to see if the current line is the start of a procedure
            if re.match(hl_start_procedure_pattern, lines[i]):
                for j in range(i, lines_length):
                    name = re.search(hl_function_name_pattern, lines[i]).group(1)
                    name.replace("PROCEDURE", "")
                    name.replace("$", "")
                    if re.search(hl_end_procedure_pattern, lines[j + 1]):
                        if 230 <= j - i <= 250:
                            procedure_230_250.append(name)
                        elif j - i > 250:
                            procedure_over_250.append(name)
                        break

            # Checks to see if current line has a Data statement
            if re.search(data_statement_pattern, lines[i]):
                hl_data_statement_counter += 1

            # Checks first to see if a block comment is present. If not, checks for single line comments.
            # Using re.IGNORECASE because some comments are in lowercase in the sample
            elif re.search(block_comment_pattern, lines[i], re.IGNORECASE):
                block_comment_counter += 1
                # It loops through next lines until '$' is found (end of the comment).
                # Then it appends the message each iteration.
                for j in range(i, lines_length):
                    comment_line_counter += 1
                    # TODO Maybe find a way to trim out tabs/repeating line numbers from message?
                    comment_text += lines[j]
                    block_comment_dictionary[i] = comment_text
                    if "$" in lines[j]:
                        # We should update loop counter so we don't double count
                        i = j
                        break
                """bc, bcl, i = comment_counter(block_comment_dictionary, comment_text, lines, i)
                block_comment_counter += bc
                #chris_blockCount = block_comments
                comment_line_counter += bcl """

            # Check if it's a single liner
            elif re.search(hl_statement_pattern, lines[i]):
                hl_statement_counter += 1
            # If statement is not a note or comment or single liner it should be a multi line statement
            # Regex just to make sure the line has some information
            elif re.search('(.*\s[0-9]+)', lines[i]):
                # Not sure what information we want to record about these multi line statements
                hl_multi_statement_counter += 1
                for j in range(i, lines_length):
                    hl_multi_statement_lines += 1
                    if "$" in lines[j]:
                        # Update counter to prevent double counting
                        i = j
                        break
            # Loop counter
            i += 1

    # assign globals for getters
    block_comments = block_comment_counter
    comment_lines = comment_line_counter
    instructions = hl_executable_counter

    # System Output:
    file_info["Number of Lines"] = lines_length
    file_info["Go-To Statements"] = goto_counter
    file_info["Notes"] = note_counter
    file_info["Block comments"] = block_comment_counter
    file_info["Block comment lines"] = comment_line_counter
    file_info["Number of non-comments"] = lines_length - comment_line_counter
    file_info["High Level CMS2 Single Line Statements"] = hl_statement_counter
    file_info["Multi-line High Level CMS2 Statements"] = hl_multi_statement_counter
    file_info["Lines of Multi-line High Level CMS2 Statements"] = hl_multi_statement_lines
    file_info["Lines containing High Level Data Statements"] = hl_data_statement_counter
    file_info["HL Executable Statements"] = hl_executable_counter
    file_info["Total lines"] = lines_length

    if file_info.__contains__("Direct Executable CMS2 Statements"):
        print ("")
    else:
        file_info["Direct Executable CMS2 Statements"] = 0

    if file_info.__contains__("Single line Direct CMS2 comments"):
        print ("")
    else:
        file_info["Single line Direct CMS2 comments"] = 0

    # if "Direct Executable CMS2 Statements" not in file_info:
    #     file_info["Direct Executable CMS2 Statements"] = 0
    #
    # if "Single line Direct CMS2 comments" not in file_info:
    #     file_info["Single line Direct CMS2 comments"] = 0


    # TODO Store this in the CMS2File object when implemented
    # timestamp = str(datetime.datetime.now())
    # print(timestamp)
    # Don't think we need this information anymore
    # fileInfo["Block Comment Dictionary"] = block_comment_counter
    # fileInfo["Note Dictionary"] = note_dictionary
    return CMS2File(name, file_info)

"""Getters"""
def getComments():
    return block_comments, comment_lines

def getInstructions():
    return instructions




"""Regex Pattern Functions"""
def comment_counter(block_comment_dictionary, comment_text, lines, current_line):
    block_comments = 0
    block_comment_lines = 0
    lines_length = len(lines)
    block_comments += 1
    # It loops through next lines until '$' is found (end of the comment).
    # Then it appends the message each iteration.
    for i in range(current_line, lines_length):
        block_comment_lines += 1
        # TODO Maybe find a way to trim out tabs/repeating line numbers from message?
        comment_text += lines[i]
        block_comment_dictionary[current_line] = comment_text
        if "$" in lines[i]:
            # We should update loop counter so we don't double count
            current_line = i
            break
    return block_comments,  block_comment_lines, current_line




"""file extension and anaylze direct"""

def check_file_extension(filename):
    file_, extension = os.path.splitext(filename)
    if extension.lower() == '.cts' or extension.lower() == '.cs2':
        valid_name = True
    else:
        valid_name = False
        print("Expected file extension .cts or .cs2, found " + extension + " in " + filename)


# Returns OrderedDict of findings
def analyze_direct(lines, procedure_over_250, procedure_230_250):
    info = OrderedDict()

    single_comments_counter = 0
    single_comment_dictionary = {}
    executable_counter = 0

    for i in range(len(lines)):
        # current_line = re.match(exec_pattern, lines[i]).group(1)
        # Not sure why this line is here. If I remember, may change.
        # For now, commented it out because not every line will be executable.
        # This caused an error.
        current_line = ""

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

        # Checks to see if the current line is the start of a procedure
        if re.match(direct_start_procedure_pattern, lines[i]):
            for j in range(i, len(lines)):
                if re.search(direct_end_procedure_pattern, lines[j+1]):
                    name = re.search(direct_function_name_pattern, lines[i]).group(1)
                    name.replace("SYS-PROC", "")
                    name.replace("$", "")
                    if 230 <= j - i <= 250:
                        procedure_230_250.append(name)
                    elif j - i > 250:
                        procedure_over_250.append(name)
                    break

    info["Direct Executable CMS2 Statements"] = executable_counter
    info["Single line Direct CMS2 comments"] = single_comments_counter
    return info


if __name__ == '__main__':
    main(sys.argv[1:])
