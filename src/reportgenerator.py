# Author: Johan Burke

from datetime import datetime

class ReportGenerator:
    """Class used to compare new and old versions of source files in the specified language"""

    def getHeaderStr(self):
        # strings to be written to text files are to be line separated by '\n'
        # on all platforms, see linesep documentation at https://docs.python.org/3/library/os.html
        self.headerStr += "\n"
        now = datetime.now()

        self.headerStr += now.strftime("%d-%b-%Y %H:%M:%S")

        # TODO: what should we put for the title?
        self.headerStr += "\t\t\tCMS-2 Source Analyzer/SAN (VAX) Version 12.01\n"

        # TODO: figure out how to number pages
        self.headerStr += "Page 1\n\n\n\t\t\t\tSource Analysis Summary\n"

        self.headerStr += "0\t\t\n"

        # may need separate string to fill in number of tabs and key in between
        self.headerStr += "\tComponent\t"

        # Don't use key for now
        for key, val in self.components.items():
            for itemHeader in val:
                self.headerStr += itemHeader + "\t" + itemHeader + "\t"
        self.headerStr += "\nMX Delimt\n"
        self.headerStr += "\tName\tType"

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
    components = {"High Level CMS-2" : ["Exec", "Data", "Comment", "NonCmt", "Other"], "CMS-2 DIRECT" : ["Exec", "Data", "Comment"]}
    gen = ReportGenerator(components)
    print(str(gen))

if __name__ == "__main__":
    main()
