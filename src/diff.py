import difflib
import re
import git
import sys
import os
from .regex import analyze
from .CMS2FileDiff import CMS2FileDiff

# README
# To run this program do one of the following:
# 1. Use command line tool and pass directory name (or filename(s)) as parameter
#       On a Mac open Terminal and navigate to this src folder. Type 'python diff.py SampleDirectory' hit enter
# 2. On top menu go to Run->Edit Configurations, and add SampleDirectory as a script parameter and hit Apply and OK

# To see sample output, make changes to the CMS2 files and save them before running diff.py

class Diff:
    # TODO: define module associated with the files
    def __init__(self):
        self.moduleName = ""
        self.diff_list = []
        self.input_files = []
        self.CPCR = []

    def getFilesFromDir(self, directory):
        file_paths = []  # List which will store all of the full filepaths.

        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)  # Add it to the list.
        return file_paths

    # Reads sys arguments to get files to run diff on
    def readInput(self, files):
        for item in files:
            if os.path.isfile(item):
                self.input_files.append(item)
            elif os.path.isdir(item):
                dir_list = self.getFilesFromDir(item)
                for dir_file in dir_list:
                    self.input_files.append(dir_file)
        #for n in range(1, len(sys.argv)):
        #    if os.path.isfile(sys.argv[n]):
        #        self.input_files.append(sys.argv[n])
        #        # print sys.argv[n]
        #    elif os.path.isdir(sys.argv[n]):
        #        list = self.getFilesFromDir(sys.argv[n])
        #        for file in list:
        #            self.input_files.append(file)

    # Analysis method. Returns a CMS2FileDiff
    def analyze(self, filename, sample1, sample2):
        diff = difflib.ndiff(sample1, sample2)

        # Accepts a '+' followed by a space.
        addition_pattern = '(\A\+ .*)'
        additions = {"Instructions": 0, "Comments": 0}

        # Accepts a '-' followed by a space.
        deletion_pattern = '(\A\- .*)'
        deletions = {"Instructions": 0, "Comments": 0}

        # Accepts a '?' followed by a space.
        modification_pattern = '(\A\? .*)'
        modifications = {"Instructions": 0, "Comments": 0}

        statement_pattern = '(.*\$)'
        direct_single_comment_pattern = '(\. .*)'
        block_comment_pattern = '([0-9]*\sCOMMENT.*)'
        # Used to help classify modification as instructions/comments
        previous = ""
        for n in diff:
            if re.search(addition_pattern, n):
                    # Order important
                    if re.search(block_comment_pattern, n):
                        additions["Comments"] += 1
                        previous = "Comments"
                    elif re.search(direct_single_comment_pattern, n):
                        additions["Comments"] += 1
                        previous = "Comments"
                    elif re.search(statement_pattern, n):
                        additions["Instructions"] += 1
                        previous = "Instructions"
                    else:
                        additions["Comments"] += 1
                        previous = "Comments"
            elif re.search(deletion_pattern, n):
                    if re.search(block_comment_pattern, n):
                        deletions["Comments"] += 1
                        previous = "Comments"
                    elif re.search(direct_single_comment_pattern, n):
                        deletions["Comments"] += 1
                        previous = "Comments"
                    elif re.search(statement_pattern, n):
                        deletions["Instructions"] += 1
                        previous = "Instructions"
                    else:
                        deletions["Comments"] += 1
                        previous = "Comments"
            elif re.search(modification_pattern, n):
                    modifications[previous]+= 1
                    additions[previous]-=1
                    deletions[previous]-=1
        # Addition/deletion patterns also show for self.modifications. Prevent double counting.
        # additions["Instructions"] -= modifications["Instructions"]
        # deletions["Instructions"] -= modifications["Instructions"]
        # additions["Comments"] -= modifications["Comments"]
        # deletions["Comments"] -= modifications["Comments"]

        file_status = "UNCHANGED"
        if(additions["Comments"] + additions["Instructions"] +
           modifications["Comments"] + modifications["Instructions"] +
           deletions["Comments"] + deletions["Instructions"] > 0):
            file_status = "CHANGED"

        return CMS2FileDiff(filename, file_status, additions, modifications, deletions)

    # Run diff between local file and same file from latest commit
    def run_diff_on_latest_commit(self):
        repo = git.Repo('.')
        for file in self.input_files:
            # Get raw text of file from latest commit
            # Split by line into array
            try:
                # If file is in repo
                oldVersionFile = repo.git.show('HEAD:'+'src/'+file).splitlines()
                # Add delimiter back in for comparison purposes
                file_content = open(file).read().splitlines()
                diff_info = self.analyze(file, oldVersionFile, file_content)
                file_info = analyze(oldVersionFile, file)

                # If code contained direct CMS2
                if hasattr(file_info, 'direct_comments') & hasattr(file_info, 'direct_exec_stmts'):
                    num_instructions = file_info.hl_exec_lines + \
                                       file_info.direct_exec_stmts + \
                                       file_info.hl_data_stmts
                    num_comments = file_info.block_comment_lines + file_info.direct_comments
                # If no direct CMS2
                else:
                    num_instructions = file_info.hl_exec_lines + file_info.hl_data_lines
                    num_comments = file_info.block_comment_lines

                diff_info.initial_size['Instructions'] = num_instructions
                diff_info.initial_size['Comments'] = num_comments
                self.diff_list.append(diff_info)
            except:
                # File not in repo (new file)
                file_info = regex.analyze(open(file).read().splitlines(), file)
                # If code contained direct CMS2
                if hasattr(file_info, 'direct_exec_stmts') & hasattr(file_info, 'direct_comments'):
                    num_instructions = file_info.hl_exec_lines + \
                                       file_info.direct_exec_stmts + \
                                       file_info.hl_data_stmts
                    num_comments = file_info.block_comment_lines + file_info.direct_comments
                # If no direct CMS2
                else:
                    num_instructions = file_info.hl_exec_lines + file_info.hl_data_lines
                    num_comments = file_info.block_comment_lines

                diff_info = CMS2FileDiff(file, "ADDED", additions={ "Instructions": num_instructions,
                                                                    "Comments": num_comments },
                                         modifications = { "Instructions": 0,
                                                                    "Comments": 0},
                                         deletions = { "Instructions": 0,
                                                                    "Comments": 0 })

                diff_info.initial_size["Instructions"] = 0
                diff_info.initial_size["Comments"] = 0
                self.diff_list.append(diff_info)

    def getDataAsString(self, fileInfo):
        return str(fileInfo.filename), str(fileInfo.status), str(fileInfo.CPCR), \
               str(fileInfo.additions), str(fileInfo.modifications), str(fileInfo.deletions)

    def __str__(self):
        result = ""
        for fileInfo in self.diff_list:
            name, status, cpcr, add, mod, dele = self.getDataAsString(fileInfo)
            result += "File: "
            result += name + "\n"
            result += "Status: " + status + "\n"
            result += "CPCR: " + cpcr + "\n"
            result += "Additions: " + add + "\n"
            result += "Modifications: " + mod + "\n"
            result += "Deletions: " + dele + "\n" + "\n"
        return result

if __name__ == "__main__":

    d = Diff()
    d.readInput(sys.argv[1:])
    d.run_diff_on_latest_commit()
    print("Diff results")
    print(str(d))
