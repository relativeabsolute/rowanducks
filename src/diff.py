import difflib
import re
import git
import sys
import os
from CMS2FileDiff import CMS2FileDiff

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

    # TODO return files in subdirectories
    # TODO only return files with correct extension
    def getFilesFromDir(self, directory):
        return [os.path.join(directory, fn) for fn in next(os.walk(directory))[2]]

    # Reads sys arguments to get files to run diff on
    def readInput(self):
        for n in range(1, len(sys.argv)):
            if os.path.isfile(sys.argv[n]):
                self.input_files.append(sys.argv[n])
                # print sys.argv[n]
            elif os.path.isdir(sys.argv[n]):
                list = self.getFilesFromDir(sys.argv[n])
                for file in list:
                    self.input_files.append(file)

    # Analysis method. Returns a CMS2FileDiff
    def analyze(self, filename, sample1, sample2):
        diff = difflib.ndiff(sample1, sample2)

        # Accepts a '+' followed by a space.
        addition_pattern = '(\+ .*)'
        additions = {"Instructions": 0, "Comments": 0}

        # Accepts a '-' followed by a space.
        deletion_pattern = '(\- .*)'
        deletions = {"Instructions": 0, "Comments": 0}

        # Accepts a '?' followed by a space.
        modification_pattern = '(\? .*)'
        modifications = {"Instructions": 0, "Comments": 0}

        statement_pattern = '(.*\$\n)'
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
                print(n)
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
                modifications[previous] += 1
        # Addition/deletion patterns also show for self.modifications. Prevent double counting.
        additions["Instructions"] -= modifications["Instructions"]
        deletions["Instructions"] -= modifications["Instructions"]
        additions["Comments"] -= modifications["Comments"]
        deletions["Comments"] -= modifications["Comments"]

        return CMS2FileDiff(filename, additions, modifications, deletions)

    # Run diff between local file and same file from latest commit
    def run_diff_on_latest_commit(self):
        repo = git.Repo('../../rowanducks/')
        for file in self.input_files:
            # Get raw text of file from latest commit
            unicode = repo.git.show('HEAD:'+'src/'+file)
            # Split by line into arry
            oldVersionFile = unicode.strip().split('\n')
            # Add delimiter back in for comparison purposes
            for line in range(0, len(oldVersionFile)):
                oldVersionFile[line]+='\n'

            self.diff_list.append(self.analyze(file, oldVersionFile, open(file).readlines()))

    def getDataAsString(self, fileInfo):
        return str(fileInfo.filename), str(fileInfo.additions), str(fileInfo.modifications), str(fileInfo.deletions)

    def __str__(self):
        result = ""
        for fileInfo in self.diff_list:
            name, add, mod, dele = self.getDataAsString(fileInfo)
            result += "File: "
            result += name + "\n"
            result += "Additions: " + add + "\n"
            result += "Modifications: " + mod + "\n"
            result += "Deletions: " + dele + "\n" + "\n"
        return result

if __name__ == "__main__":

    d = Diff()
    d.readInput()
    d.run_diff_on_latest_commit()
    print("Diff results")
    print(str(d))
