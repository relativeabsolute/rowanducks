# Not sure if we'll use but including anyway
class CMS2FileDiff:

    def __init__(self, filename, status, additions,
                 modifications={"Instructions":0, "Comments": 0},
                 deletions={"Instructions":0, "Comments": 0}):
        self.filename = filename
        self.moduleName = ""
        self.additions = additions
        self.modifications = modifications
        self.deletions = deletions
        # this will contain initial number of instructions and comments
        self.initial_size = {}
        self.status = status
        # Default value for now
        self.CPCR = "UNSPECIFIED"
