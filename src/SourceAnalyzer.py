# Author: Johan Burke

import sys
from .regex import main as regex_main
from .CMS2File import CMS2File

from datetime import datetime

class SourceAnalyzer:
    @property
    def header_str(self):
        return self._header_str

    @property
    def data_str(self):
        return self._data_str

    def __set_header_str(self):
        now = datetime.now()

        date_str = now.strftime("%d-%b-%Y %H:%M:%S")

        date_title = "{0:<{width}}".format(date_str, width=int(self.columns/2))
        date_title += "{0:^{width}}".format('CMS-2 Source Analyzer/SAN (VAX) Version 12.01', width=int(self.columns/2))

        self._header_str = date_title + "\n"

        self._header_str += "{0:^{width}}\n".format('Source Analysis Summary', width=int(self.columns))
        
        under_str = "{0:{fill}<{width}}".format("", fill=" ", width=int(self.columns/10))
        under_str += "+{0:{fill}^{width}}+".format("High Level CMS-2", fill="-", width=int(self.columns/2) - 5)
        under_str += " +{0:{fill}^{width}}+".format("CMS-2 DIRECT", fill="-", width=int(self.columns / 6) + 1)
        under_str += "  +{0:{fill}^{width}}+".format("Total", fill="-", width=int(self.columns / 10))

        self._header_str += under_str + "\n"

        column_headings = "{0:<{width}}".format('Component', width=int(self.columns/10))
        column_headings += "{0:<{width}}".format('Exec', width=int(self.columns/15))
        column_headings += "{0:<{width}}".format('Exec', width=int(self.columns/15))
        column_headings += "{0:<{width}}".format('Data', width=int(self.columns/15))
        column_headings += "{0:<{width}}".format('Data', width=int(self.columns/15))
        column_headings += "{0:<{width}}".format('Comment', width=int(self.columns/15))
        column_headings += "{0:<{width}}".format('Comment', width=int(self.columns/15))
        column_headings += "{0:<{width}}".format('NonCmt', width=int(self.columns/15))
        column_headings += "{0:<{width}}".format('Other', width=int(self.columns/15))
        column_headings += "{0:<{width}}".format('Exec', width=int(self.columns/15))
        column_headings += "{0:<{width}}".format('Data', width=int(self.columns/15))
        column_headings += "{0:<{width}}".format('Comment', width=int(self.columns/15))
        column_headings += "{0:<{width}}".format('Exec', width=int(self.columns/15))
        column_headings += "{0:<{width}}".format('Source', width=int(self.columns/15))
        column_headings += "{0:<{width}}".format('CSWTC', width=int(self.columns/15))
        column_headings += "{0:<{width}}".format('MX Delimt', width=int(self.columns/15))

        self._header_str += column_headings + '\n'
        
        column_types = "{0:<{width}}".format('Name', width=int(self.columns/20))
        column_types += "{0:<{width}}".format('Type', width=int(self.columns/20))
        column_types += "{0:<{width}}".format('Stmts', width=int(self.columns/15))
        column_types += "{0:<{width}}".format('Lines', width=int(self.columns/15))
        column_types += "{0:<{width}}".format('Stmts', width=int(self.columns/15))
        column_types += "{0:<{width}}".format('Lines', width=int(self.columns/15))
        column_types += "{0:<{width}}".format('Stmts', width=int(self.columns/15))
        column_types += "{0:<{width}}".format('Lines', width=int(self.columns/15))
        column_types += "{0:<{width}}".format('Lines', width=int(self.columns/15))
        column_types += "{0:<{width}}".format('Stmts', width=int(self.columns/15))
        column_types += "{0:<{width}}".format('Stmts', width=int(self.columns/15))
        column_types += "{0:<{width}}".format('Stmts', width=int(self.columns/15))
        column_types += "{0:<{width}}".format('Lines', width=int(self.columns/15))
        column_types += "{0:<{width}}".format('Stmts', width=int(self.columns/15))
        column_types += "{0:<{width}}".format('Lines', width=int(self.columns/15))
        column_types += "{0:<{width}}".format('Stmts', width=int(self.columns/15))
        column_types += "{0:<{width}}".format('LV Stmts', width=int(self.columns/15))
        
        self._header_str += column_types + '\n'
        self._header_str += "{0:{fill}^{width}}".format("", fill="-", width=int(self.columns))


    def __format(self):
        self.__set_header_str()
        #self.__set_data_str()

    def __init__(self, file_list, columns = 160):
        self._header_str = ""
        self._data_str = ""
        self.columns = columns
        self._data_str = ""
        self.__file_list = file_list
        self.__format()

    def __str__(self):
        return self.header_str

def main(args):
    file_list = regex_main(args)
    san = SourceAnalyzer(args)
    print(str(san))

if __name__ == "__main__":
    main(sys.argv[1:])
