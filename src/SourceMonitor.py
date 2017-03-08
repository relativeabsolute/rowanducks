# Author: Johan Burke

from datetime import datetime

class SourceMonitor:
    def get_header_string(self):
        self.header_string = "\tSRCMON - SOURCE CODE MONITOR, VERSION 07.00"
        
        now = datetime.now()

        date_title = now.strftime("%d/%b/%Y")

        self.header_string += "\t\t\t\t\t\t\t" + date_title
        self.header_string += "\n\t\t\t\t\t\t\t\t\t\t\t\t\tPAGE 1\n"

        class_name = "///CLASS NAME HERE///"
        self.header_string += "\t\t\t\t\t" + class_name + "\n"

    def __init__(self):
        self.get_header_string()

def main():
    sm = SourceMonitor()
    print(sm.header_string)

if __name__ == "__main__":
    main()
