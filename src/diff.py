import difflib
import re
from CMS2FileDiff import CMS2FileDiff

class Diff:
    # TODO: define module associated with the files
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2
        self.moduleName = ""
    
    def run_diff(self):
        self.diff = difflib.ndiff(open(self.file1).readlines(),open(self.file2).readlines())

        # Accepts a '+' followed by a space.
        addition_pattern = '(\+ .*)'
        self.additions = {"Instructions": 0, "Comments":0}
        self.instructionAdditions = 0
        self.commentAdditions = 0
        # Accepts a '-' followed by a space.
        deletion_pattern = '(\- .*)'
        self.deletions = {"Instructions": 0, "Comments":0}
        self.instructionDeletions = 0
        self.commentDeletions = 0
        # Accepts a '?' followed by a space.
        modification_pattern = '(\? .*)'
        self.modifications = {"Instructions": 0, "Comments":0}
        self.instructionModifications = 0
        self.commentModifications = 0

        statement_pattern = '(.*\$)'
        direct_single_comment_pattern = '(\. .*)'
        block_comment_pattern = '([0-9]*\sCOMMENT.*)'
        for n in self.diff:
            if re.search(addition_pattern, n):
                # Order important
                if re.search(block_comment_pattern, n):
                    self.additions["Comments"]+=1
                elif re.search(direct_single_comment_pattern, n):
                    self.additions["Comments"] += 1
                elif re.search(statement_pattern, n):
                    self.additions["Instructions"] += 1
                else:
                    self.additions["Comments"] += 1
            elif re.search(deletion_pattern, n):
                if re.search(block_comment_pattern, n):
                    self.deletions["Comments"] += 1
                elif re.search(direct_single_comment_pattern, n):
                    self.deletions["Comments"] += 1
                elif re.search(statement_pattern, n):
                    self.deletions["Instructions"] += 1
                else:
                    self.deletions["Comments"] += 1
            elif re.search(modification_pattern, n):
                if re.search(block_comment_pattern, n):
                    self.modifications["Comments"] += 1
                elif re.search(direct_single_comment_pattern, n):
                    self.modifications["Comments"] += 1
                elif re.search(statement_pattern, n):
                    self.modifications["Instructions"] += 1
                else:
                    self.modifications["Comments"] += 1
        # Addition/deletion patterns also show for self.modifications. Prevent double counting.
        self.additions["Instructions"]-=self.modifications["Instructions"]
        self.deletions["Instructions"]-=self.modifications["Instructions"]
        self.additions["Comments"]-=self.modifications["Comments"]
        self.deletions["Comments"]-=self.modifications["Comments"]

    def __str__(self):
        result = "Additions: " + str(self.additions) + "\n"
        result += "Modifications: " + str(self.modifications) + "\n"
        result += "Deletions: " + str(self.deletions) + "\n"
        return result

if __name__ == "__main__":
    file1 = "CMS-2_HighLevel2.txt"
    file2 = "CMS-2_HighLevel2_Edited.txt"

    d = Diff(file1, file2)
    d.run_diff()
    print("Diff results")
    print(str(d))
