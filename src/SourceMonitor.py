# Author: Johan Burke

from datetime import datetime
from diff import Diff

class SourceMonitor:
    def get_header_string(self):
        # header string represents the title and column information of the report
        self.header_string = "\tSRCMON - SOURCE CODE MONITOR, VERSION 07.00"
        
        now = datetime.now()

        date_title = now.strftime("%d/%b/%Y")

        self.header_string += "\t\t\t\t\t\t\t\t\t\t\t" + date_title
        self.header_string += "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tPAGE 1\n"

        class_name = "///CLASS NAME HERE///"
        self.header_string += "\t\t\t\t\t\t\t" + class_name + "\n"

        column_names = "MODULE\t\t\t\t\t|FILE STATUS|\tINITIAL SIZE\t| CPCR\t\t\t"
        column_names += "ADDITIONS\tMODIFICATIONS\t|\tDELETIONS\n"
        self.header_string += column_names

        underline_str = "----------------------------------------|-----------|-------------------|"
        underline_str += "-------------------------------------------------------|----------------"
        self.header_string += underline_str

    def get_rows(self):
        # main string contains the rows of data of the report
        self.main_string = ""
        for diff in self.diffs:
            self.main_string += diff.moduleName + ":\n"
            self.main_string += "\t" + diff.file1 + "\t\t| CHANGED   |\t\t\t| UNSPECIFIED\t"


    def __init__(self, diffs):
        self.get_header_string()
        self.diffs = diffs
        self.get_rows()

def main():
    file1 = "CMS-2_HighLevel_2.txt"
    file2 = "CMS-2_HighLevel_Edited.txt"

    d1 = Diff(file1, file2)
    d1.moduleName = "CMS-2_HighLevel"

    diffs = [d1]

    sm = SourceMonitor(diffs)
    print(sm.header_string)
    print(sm.main_string)

if __name__ == "__main__":
    main()
