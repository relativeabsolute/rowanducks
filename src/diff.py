import difflib
import re

file1 = "CMS-2_HighLevel_2.txt"
file2 = "CMS-2_HighLevel_Edited.txt"

diff = difflib.ndiff(open(file1).readlines(),open(file2).readlines())

# Accepts a '+' followed by a space and any number of any characters until line ends to extract in-line comment.
addition_pattern = '(\+ .*)'
additions = 0
# Accepts a '-' followed by a space and any number of any characters until line ends to extract in-line comment.
deletion_pattern = '(\- .*)'
deletions = 0
# Accepts a '?' followed by a space and any number of any characters until line ends to extract in-line comment.
modification_pattern = '(\? .*)'
modifications = 0

for n in diff:
    if re.search(addition_pattern, n):
        additions+=1
    elif re.search(deletion_pattern, n):
        deletions+=1
    elif re.search(modification_pattern, n):
        modifications+=1
# Addition/deletion patterns also show for modifications. Prevent double counting.
additions-=modifications
deletions-=modifications

print
print("Additions: " + str(additions))
print
print("Modifications: " + str(modifications))
print
print ("Deletions: " + str(deletions))
print
