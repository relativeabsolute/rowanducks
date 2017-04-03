# Author: Johan Burke

import time
from datetime import datetime
from collections import OrderedDict


class Report:
    """ The Class is used to compare new and old versions of source files in the specified language."""

    # Pycharm tells me that this method might be static.
    def get_section_string(self, categories_string, section_name):
        # A section string is divided the following way:
        # -start and end are denoted by '+'s
        # -the +'s are followed/preceded by an equal number of '-'s
        # -the -'s are followed/preceded by a space with the name of the section in between

        # This doesn't give the true length of the string since \t would be considered one character
        # totalLen = len(categoriesStr)

        total_length = 0
        tab_length = 4
        for index in range(len(categories_string)):
            if categories_string[index] == '\t':
                to_add = tab_length - (index % tab_length)
                total_length += to_add
            else:
                total_length += 1
        # TODO: note this breaks if the sectionName contains a '\t' character
        name_length = len(section_name)

        result = "+"
        num_dashes = int(total_length / 2) - int(name_length / 2 + 1) 
        dashes = "-" * num_dashes
        result += dashes + " " + section_name + " " + dashes + "+"
        return result

    def get_header_string(self):
        # Strings are written to text files. Each line separated by '\n'.
        # On all platforms, see linesep documentation at https://docs.python.org/3/library/os.html
        self.header_string += "\n"
        now = datetime.now()

        date_title = now.strftime("%d-%b-%Y %H:%M:%S")

        # TODO: what should we put for the title?
        date_title += "\t\t\tCMS-2 Source Analyzer/SAN (VAX) Version 12.01\n"

        # TODO: figure out how to number pages
        date_title += "Page 1\n\n\n\t\t\t\tSource Analysis Summary\n"

        # Denotes High Level CMS-2, CMS-2 DIRECT, or something else
        version = "0\t\t"

        # We may need to separate string to fill in the number of tabs and keys in between.
        categories_header = "\t\tComponent\t"
        fields = "\t"

        categories = ""
        categories_start = 0
        section_string = ""
        for key, val in self.components.items():
            for itemKey, itemVal in val.items():
                for field in itemVal:
                    categories += itemKey + "\t"
                    fields += field + "\t"
            if key != "":
                categories += "\t"
                fields += "\t"
                categories_length = len(categories)
                section_string += self.get_section_string(categories[categories_start:categories_length], key) + "\t"
                categories_start = categories_length

        self.header_string = date_title + version + "\t" + section_string + "\n" + categories_header + categories
        self.header_string += "\n"
        self.header_string += "\tName\tType" + fields

        return self.header_string

    # Return a string representation of this Report, a la java toString
    def __str__(self):
        result = "Report:\n"
        # Just testing stuff?
        # result += "Header string:\n"
        # result += "----------------\n"
        # result += self.header_string
        result += "\n----------------\n"
        result += "Complete report string:\n"
        result += "----------------"
        result += self.report_string
        return result

    def __init__(self, components):
        self.components = components
        self.header_string = ""
        self.report_string = self.get_header_string()

    def write_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.report_string)



def main():
    # TODO: what is the best way to structure this?
    # Main will currently print "Stmts" and "Lines" for each type, but that's not the case in the sample report.
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

    components["Total"] = OrderedDict()
    components["Total"]["Exec"] = ["Stmts"]
    components["Total"]["Source"] = ["Lines"]

    components[""] = OrderedDict()
    components[""]["CSWTC"] = ["Stmts"]
    components[""]["MX"] = ["LV"]
    components[""]["Delimt"] = ["Stmts"]

    beforeTime = time.time()
    gen = Report(components)
    afterTime = time.time()
    print(str(gen))

    # Sample data string for the sprint review
    # TODO use python module tabulate to make report table
    print("CMS2YSample\tSYS\t\t1\t\t2\t\t3\t\t3\t\t5\t\t6\t\t7\t\t8\t\t\t9\t\t10\t\t11\t\t\t12\t\t13\t\t\t14\t\t15\t\t16")
    print("CMS2YHL  \tSYS\t\t1\t\t2\t\t3\t\t3\t\t5\t\t6\t\t7\t\t8\t\t\t9\t\t10\t\t11\t\t\t12\t\t13\t\t\t14\t\t15\t\t16")

    # Grand Summary
    # Eventually would like to turn this into a method
    # create array to hold occurrences - hardcoded to show template, will be changed.
    occurrences = [0,0,0,0,0,0,4,0,0,11]
    # create array to hold modules detected - hardcoded to show template, will be changed.
    modules_detected = [0,0,0,0,0,0,2,0,0,2]
    print("\t\t\t\t\t\t\t\t\t\t\tSource Review Summary")
    print("\t\t\t\t\t\t\t\t\t\t\t\tGrand Summary")
    print("\t\t\t\t\t\t\t\t\t\t\t  Full class/Source")
    print ("0CPS-3.1.3 5.1.5 GOTO statement found \t\t\t\t\t\t\t\t\t ", occurrences[0], "occurrence(s) in ", modules_detected[0], " module(s) detected")
    print ("0CPS-3.1.3 5.1.1 SYSTEM not structured \t\t\t\t\t\t\t\t\t ", occurrences[1], "occurrence(s) in ", modules_detected[1], " module(s) detected")
    print ("0CPS-3.1.3 5.1.3 Misplaced END-SYSTEM \t\t\t\t\t\t\t\t\t ", occurrences[2], "occurrence(s) in ", modules_detected[2], " module(s) detected")
    print ("0CPS-3.1.3 5.1.3 Incorrect file extension \t\t\t\t\t\t\t\t ", occurrences[3], "occurrence(s) in ", modules_detected[3], " module(s) detected")
    print ("0CPS-3.1.3 5.1.3 Multiple components in file \t\t\t\t\t\t\t ", occurrences[4], "occurrence(s) in ", modules_detected[4], " module(s) detected")
    print ("0CPS-3.1.3 5.1.3 Component name/file name mismatch \t\t\t\t\t\t ", occurrences[5], "occurrence(s) in ", modules_detected[5], " module(s) detected")
    print ("0CPS-3.1.3 5.1.2 System code letter mismatch \t\t\t\t\t\t\t ", occurrences[6], "occurrence(s) in ", modules_detected[6], " module(s) detected")
    print("\t\t\t\t MDBA4E1 \t MTD4E1")
    print ("0CPS-3.1.3 5.1.2 Module mnemonic mismatch \t\t\t\t\t\t\t\t ", occurrences[7], "occurrence(s) in ", modules_detected[7], " module(s) detected")
    print ("0CPS-3.1.3 5.1.2 Non-standard prime procedure name \t\t\t\t\t\t ", occurrences[8], "occurrence(s) in ", modules_detected[8], " module(s) detected")
    print ("0CPS-3.1.3 5.1.1 Component abstract not found \t\t\t\t\t\t\t ", occurrences[9], "occurrence(s) in ", modules_detected[9], " module(s) detected")

    # TODO: convert to human readable time format
    print("\nBefore time = " + str(time.ctime(beforeTime)))
    print("After time = " + str(time.ctime(afterTime)))
    print("Time spent generating report = " + str(afterTime - beforeTime))


if __name__ == "__main__":
    main()
