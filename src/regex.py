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
from CMS2FileInfo import CMS2FileInfo

sample_file = "/SampleDirectory/CMS2YSample.txt"
sample_HL_file = "/SampleDirectory/CMS-2_HighLevel_2.txt"
valid_name = False

# Accepts 'X' followed by any number of digits or 'A/' followed by any number of digits.
exec_pattern = '(X[0-9]+|A/[0-9]+)'

# Accepts anything that ends in $
HL_statement_pattern ='(.*\$)'

# Accepts a '.' followed by any number of any characters until line ends to extract in-line comment.
single_comment_pattern = '(\. .*)'

# Accepts any digits followed by any number of white spaces, followed by 'COMMENT', followed by any characters.
block_comment_pattern = '([0-9]*\sCOMMENT.*)'

# Accepts any characters followed by 'SYS-PROC' followed by any characters and a '$'
direct_start_procedure_pattern = '(\.*SYS-PROC\s*\$)'

# Accepts any characters followed by 'END-SYS-PROC' followed by any characters and a '$'
direct_end_procedure_pattern = '(\.*END-SYS-PROC.*\$)'

# Accepts any characters followed by 'PROCEDURE' followed by any characters and a '$'
HL_start_procedure_pattern = '(\.*PROCEDURE.*\$)'

# Accepts any characters followed by 'RETURN' followed by any characters and a '$'
HL_end_procedure_pattern = '(\.*RETURN.*\$)'

# The three major types of data statements are switches, variables, and aggregates
data_statement_pattern = '((.*SET.*TO.*\$)|(.*SWITCH.*\$.*END-SWITCH.*\$)|(.*FIELD\b\S*\b.*\$))'

# Accepts two single apostrophes (''), followed by any characters/digits, followed by two single apostrophes.
note_pattern = '(\'\'[\w|\s|-]*\'\')'


def main():
    finished = False
    input_files = []
    list_CMS2FileInfo = []
    # Takes arguments (filenames) from command line separated by spaces
    # Could update this to take a directory and analyze all files in directory
    for n in range(1, len(sys.argv)):
        if os.path.isfile(sys.argv[n]):
            input_files.append(sys.argv[n])
            #print sys.argv[n]
        elif os.path.isdir(sys.argv[n]):
            list = getFilesFromDir(sys.argv[n])
            for file in list:
                input_files.append(file)

    for location in input_files:
        list_CMS2FileInfo.append(split_file(location))
    for fileData in list_CMS2FileInfo:
        print fileData.printString()

# TODO return files in subdirectories
# TODO only return files with correct extension
def getFilesFromDir(directory):
    return [os.path.join(directory,fn) for fn in next(os.walk(directory))[2]]

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

    HL_data_statement_counter = 0
    procedure_over_250 = []
    procedure_230_250 = []


    # Changed the "for in" loop to while so we can change loop counter when needed (see lines 100, 115)
    i = 0
    fileInfo = OrderedDict()
    while (i < len(lines)):
        current_line = ""
        comment_text = ""
        statement_text = ""

        # Detects Direct CMS-2 code blocks and sends the entire block to be analyzed.
        if re.search('(DIRECT\s*\$)', lines[i]):
            for j in range(i, len(lines)):
                if re.search("(CMS-2\s*\$)", lines[j+1]):
                    fileInfo.update(analyze_direct(lines[i:j], procedure_over_250, procedure_230_250))
                    i = j + 1  # Update loop counter so we don't analyze code block more than once
                    break
            i = j+1 # Prevent infinite loop if code sample improperly formatted
        # This else handles all high-level code.
        else:
            if 'GOTO' in lines[i]:
                # I'm not sure how to handle this yet, but the sample output keeps track of them.
                goto_counter += 1
                #print("GOTO detected on line " + str(current_line))

            # Checks to see if the current line contains a programmer's note.
            if re.search(note_pattern, lines[i]):
                note_counter += 1
                # Adds note to note_dictionary.
                comment_text = re.search(note_pattern, lines[i]).group(1)
                note_dictionary[current_line] = comment_text

            # Checks to see if the current line is the start of a procedure
            if re.match(HL_start_procedure_pattern, lines[i]):
                for j in range(i, len(lines)):
                    if re.search(HL_end_procedure_pattern, lines[j + 1]):
                        if 230 <= j - i <= 250:
                            procedure_230_250.append(lines[i])
                        elif j - i > 250:
                            procedure_over_250.append(lines[i])
                        break

            # Checks to see if current line has a Data statement
            if re.search(data_statement_pattern, lines[i]):
                HL_data_statement_counter += 1

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

    # System Output:
    fileInfo["Number of Lines"] = len(lines)
    fileInfo["Go-To Statements"] = goto_counter
    fileInfo["Notes"] = note_counter
    fileInfo["Block comments"] = block_comment_counter
    fileInfo["Block comment lines"] = block_comment_line_counter
    fileInfo["Number of non-comments"] = len(lines) - block_comment_line_counter
    fileInfo["High Level CMS2 Single Line Statements"] = HL_statement_counter
    fileInfo["Multi-line High Level CMS2 Statements"] = HL_multi_statement_counter
    fileInfo["Lines of Multi-line High Level CMS2 Statements"] = HL_multi_statement_lines
    fileInfo["Lines containing High Level Data Statements"] = HL_data_statement_counter
    fileInfo["Total lines"] = len(lines)

    # TODO Store this in the CMS2File object when implemented
    #timestamp = str(datetime.datetime.now())
    #print(timestamp)
    # Don't think we need this information anymore
    # fileInfo["Block Comment Dictionary"] = block_comment_counter
    # fileInfo["Note Dictionary"] = note_dictionary
    return CMS2FileInfo(name, fileInfo)


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

        # Checks to see if the current line is the start of a procedure
        if re.match(direct_start_procedure_pattern, lines[i]):
            for j in range(i, len(lines)):
                if re.search(direct_end_procedure_pattern, lines[j+1]):
                    if 230 <= j - i <= 250:
                        procedure_230_250.append(lines[i])
                    elif j - i > 250:
                        procedure_over_250.append(lines[i])
                    break

    info["Executable CMS2 lines"] = executable_counter
    info["Single line Direct CMS2 comments"] = single_comments_counter
    return info

# TODO everything
def compare_files(original, modified):
    return


if __name__ == '__main__':
    main()
