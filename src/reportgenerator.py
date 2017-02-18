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

    def __init__(self):
        self.headerStr = ""
        self.reportStr = self.getHeaderStr()

    def writeToFile(self, filename):
        with open(filename, 'w') as f:
            f.write(self.reportStr)

def main():
    gen = ReportGenerator()
    print(str(gen))

if __name__ == "__main__":
    main()
