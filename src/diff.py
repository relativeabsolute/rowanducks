import difflib
import re

class Diff:
    # TODO: define module associated with the files
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2
        self.moduleName = ""
    
    def run_diff(self):
        self.diff = difflib.ndiff(open(self.file1).readlines(),open(self.file2).readlines())

        # Accepts a '+' followed by a space and any number of any characters until line ends to extract in-line comment.
        addition_pattern = '(\+ .*)'
        self.additions = 0
        # Accepts a '-' followed by a space and any number of any characters until line ends to extract in-line comment.
        deletion_pattern = '(\- .*)'
        self.deletions = 0
        # Accepts a '?' followed by a space and any number of any characters until line ends to extract in-line comment.
        modification_pattern = '(\? .*)'
        self.modifications = 0

        for n in self.diff:
            if re.search(addition_pattern, n):
                self.additions+=1
            elif re.search(deletion_pattern, n):
                self.deletions+=1
            elif re.search(modification_pattern, n):
                self.modifications+=1
        # Addition/deletion patterns also show for self.modifications. Prevent double counting.
        self.additions-=self.modifications
        self.deletions-=self.modifications

    def __str__(self):
        result = "Additions: " + str(self.additions) + "\n"
        result += "Modifications: " + str(self.modifications) + "\n"
        result += "Deletions: " + str(self.deletions) + "\n"
        return result

if __name__ == "__main__":
    file1 = "CMS-2_HighLevel_2.txt"
    file2 = "CMS-2_HighLevel_Edited.txt"

    d = Diff(file1, file2)
    d.run_diff()
    print("Diff results")
    print(str(d))
