# Author: Johan Burke

from datetime import datetime
from collections import OrderedDict

class ReportGenerator:
    """Class used to compare new and old versions of source files in the specified language"""

    def getHeaderStr(self):
        # strings to be written to text files are to be line separated by '\n'
        # on all platforms, see linesep documentation at https://docs.python.org/3/library/os.html
        self.headerStr += "\n"
        now = datetime.now()

        dateTitle = now.strftime("%d-%b-%Y %H:%M:%S")

        # TODO: what should we put for the title?
        dateTitle += "\t\t\tCMS-2 Source Analyzer/SAN (VAX) Version 12.01\n"

        # TODO: figure out how to number pages
        dateTitle += "Page 1\n\n\n\t\t\t\tSource Analysis Summary\n"

        # denotes High Level CMS-2, CMS-2 DIRECT, or something else
        version = "0\t\t"

        # may need separate string to fill in number of tabs and key in between
        categories = "\tComponent\t"
        fields = "\t"

        # Don't use key for now
        for key, val in self.components.items():
            for itemKey, itemVal in val.items():
                for field in itemVal:
                    categories += itemKey + "\t"
                    fields += field + "\t"
        
        self.headerStr = dateTitle + version + "\n" + categories
        self.headerStr += "\nMX Delimt\n"
        self.headerStr += "\tName\tType" + fields

        return self.headerStr

    # return a string representation of this Report, a la java toString
    def __str__(self):
        result = "Report:\n"
        result += "Header string:\n"
        result += "----------------\n"
        result += self.headerStr
        result += "\n----------------\n"
        result += "Complete report string:\n"
        result += "----------------"
        result += self.reportStr
        return result

    def __init__(self, components):
        self.components = components
        self.headerStr = ""
        self.reportStr = self.getHeaderStr()

    def writeToFile(self, filename):
        with open(filename, 'w') as f:
            f.write(self.reportStr)

def main():
    # TODO: what is the best way to structure this?
    # Currently will print "Stmts" and "Lines" for each type, but that's not the case in the sample report
    components = OrderedDict()
    components["High Level CMS-2"] = OrderedDict()
    components["High Level CMS-2"]["Exec"] = ["Stmts", "Lines"]
    components["High Level CMS-2"]["Data"] = ["Stmts", "Lines"]
    components["High Level CMS-2"]["Comment"] = ["Stmts", "Lines"]
    components["High Level CMS-2"]["NonCmt"] = ["Lines"]
    components["High Level CMS-2"]["Other"] = ["Stmts"]

    components["CMS-2 DIRECT"] = OrderedDict()
    components["CMS-2 DIRECT"]["Exec"] = ["Stmts"]
    components["CMS-2 DIRECT"]["Data"] = ["Stmts"]
    components["CMS-2 DIRECT"]["Comment"] = ["Lines"]

    gen = ReportGenerator(components)
    print(str(gen))

if __name__ == "__main__":
    main()
