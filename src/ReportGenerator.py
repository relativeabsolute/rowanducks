# Author: Johan Burke

from datetime import datetime
from collections import OrderedDict


class ReportGenerator:
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
                total_length += tab_length - (index % tab_length)
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
        categories_header = "\tComponent\t"
        fields = "\t"

        categories = ""
        categories_start = 0
        section_string = ""
        for key, val in self.components.items():
            for itemKey, itemVal in val.items():
                for field in itemVal:
                    categories += itemKey + "\t"
                    fields += field + "\t"
            categories_length = len(categories)
            section_string += self.get_section_string(categories[categories_start:categories_length], key) + "\t"
            categories_start = categories_length

        self.header_string = date_title + version + "\t" + section_string + "\n" + categories_header + categories
        self.header_string += "\nMX Delimt\n"
        self.header_string += "\tName\tType" + fields

        return self.header_string

    # Return a string representation of this Report, a la java toString
    def __str__(self):
        result = "Report:\n"
        result += "Header string:\n"
        result += "----------------\n"
        result += self.header_string
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

    gen = ReportGenerator(components)
    print(str(gen))


if __name__ == "__main__":
    main()
