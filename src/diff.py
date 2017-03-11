import difflib

file1 = "CMS-2_HighLevel_2.txt"
file2 = "CMS-2_HighLevel_Edited.txt"

diff = difflib.ndiff(open(file1).readlines(),open(file2).readlines())

print ''.join(diff)