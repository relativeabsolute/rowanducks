import difflib

file1 = "CMS-2_HighLevel_2.txt"
file2 = "CMS-2_HighLevel_Edited.txt"

diff = difflib.ndiff(open(file1).readlines(),open(file2).readlines())

print ''.join(diff)

additions = 0
modifications = 0
deletions = 0

# Accepts a '+' followed by any number of any characters until line ends to extract in-line comment.
addition_pattern = '(+. .*)'
# Accepts a '-' followed by any number of any characters until line ends to extract in-line comment.
deletion_pattern = '(-. .*)'
# Accepts a '?' followed by any number of any characters until line ends to extract in-line comment.
modification_pattern = '(?. .*)'