# Not sure if we'll use but including anyway
class CMS2FileDiff:
    def __init__(self, filename, status, additions, modifications, deletions):
        self.filename = filename
        self.moduleName = ""
        self.additions = additions
        self.modifications = modifications
        self.deletions = deletions
        self.status = status
        # Default value for now
        self.CPCR = "UNSPECIFIED"