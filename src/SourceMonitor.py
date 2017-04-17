# Author: Johan Burke

import os.path
from datetime import datetime
from diff import Diff


class SourceMonitor:
    def get_header_string(self):
        # header string represents the title and column information of the report
        self.header_string = "\tSRCMON - SOURCE CODE MONITOR, VERSION 07.00"

        now = datetime.now()

        date_title = now.strftime("%d/%b/%Y")

        # self.header_string += "\t\t\t\t\t\t\t\t\t\t\t" + date_title
        # self.header_string += "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tPAGE 1\n"

        self.header_string = "{0:<{width}}".format('SRCMON - SOURCE CODE MONITOR, VERSION 07.00',
                                                   width=int(self.columns))
        self.header_string += "\n{0:>{width}}".format(date_title, width=int(self.columns - self.columns / 6))
        self.header_string += ("\n{0:>{width}}").format('PAGE 1', width=int(self.columns - self.columns / 6))

        class_name = "///CLASS NAME HERE///"
        self.header_string += ("\n{0:^{width}}").format(class_name, width=self.columns)
        self.header_string += "\n"

        column_names = "{0:<{width}}".format('MODULE', width=int(self.columns / 4))
        column_names += "{0:^{width}}".format('|FILE STATUS|', width=int(self.columns / 12))

        column_names += "{0:^{width}}".format('INITIAL SIZE', width=int(self.columns / 8))
        column_names += "| {0:<{width}}".format('CPCR', width=int(self.columns / 8))

        column_names += "{0:<{width}}".format('ADDITIONS', width=int(self.columns / 10))
        column_names += "{0:<{width}}|".format('MODIFICATIONS', width=int(self.columns / 10))
        column_names += "{0:>{width}}".format('DELETIONS', width=int(self.columns / 10))

        self.header_string += column_names + "\n"

        underline_str = "{0:{fill}<{width}}".format("", fill="-", width=int(self.columns / 4))
        underline_str += "|{0:{fill}<{width}}|".format("", fill="-", width=int(self.columns / 12) - 2)
        underline_str += "{0:{fill}<{width}}".format("", fill="-", width=int(self.columns / 8))
        underline_str += "|{0:{fill}<{width}}".format("", fill="-", width=int(self.columns / 8 + self.columns / 5 + 1))
        underline_str += "|{0:{fill}<{width}}".format("", fill="-", width=int(self.columns / 8))

        self.header_string += underline_str

    def get_rows(self):
        # main string contains the rows of data of the report
        self.main_string = ""
        for fileInfo in self.diff.diff_list:
            name, status, cpcr, add, mod, dele = self.diff.getDataAsString(fileInfo)
            name = os.path.split(name)[1]
            # self.main_string += name + ": " + add + mod + dele
            self.main_string += "{0:<{width}}".format(name, width=int(self.columns / 4))
            self.main_string += "|{0:^{width}}|".format(status, width=int(self.columns / 12) - 2)
            self.main_string += "{0:<{width}}".format(str(fileInfo.initial_size["Instructions"]) + "I",
                                                      width=int(self.columns / 16))
            self.main_string += "{0:<{width}}".format(str(fileInfo.initial_size["Comments"]) + "C",
                                                      width=int(self.columns / 16))
            self.main_string += "|{0:^{width}}".format(" UNSPECIFIED", width=int(self.columns / 8))
            self.main_string += "{0:<{width}}".format(str(fileInfo.additions["Instructions"]) + "I",
                                                      width=int(self.columns / 20))
            self.main_string += "{0:<{width}}".format(str(fileInfo.additions["Comments"]) + "C",
                                                      width=int(self.columns / 20))
            self.main_string += "{0:<{width}}".format(str(fileInfo.modifications["Instructions"]) + "I",
                                                      width=int(self.columns / 20))
            self.main_string += "{0:<{width}}".format(str(fileInfo.modifications["Comments"]) + "C",
                                                      width=int(self.columns / 20))
            self.main_string += " |{0:>{width}}".format(str(fileInfo.deletions["Instructions"]) + "I",
                                                        width=int(self.columns / 20))
            self.main_string += "{0:>{width}}".format(str(fileInfo.deletions["Comments"]) + "C",
                                                      width=int(self.columns / 20))
            # self.main_string += "\t" + "\t| CHANGED   |\t\t\t\t\t| UNSPECIFIED\t\n"
            self.main_string += "\n"
            # for diff in self.diffs:
            #    self.main_string += diff.moduleName + ":\n"
            #    self.main_string += "\t" + diff.file1 + "\t| CHANGED   |\t\t\t\t\t| UNSPECIFIED\t"

    def __init__(self, diff):
        self.columns = 160
        self.get_header_string()
        self.diff = diff
        self.get_rows()


def main():
    d1 = Diff()
    d1.readInput()
    d1.run_diff_on_latest_commit()
    # diffs = [d1]

    print("Diff output: ")
    print(str(d1))

    sm = SourceMonitor(d1)
    print(sm.header_string)
    print(sm.main_string)


if __name__ == "__main__":
    main()