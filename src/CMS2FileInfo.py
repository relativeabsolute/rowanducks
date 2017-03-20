
class CMS2FileInfo:
    # TODO: define module associated with the files
    def __init__(self, fileName, fileData):
        self.FileName = fileName
        self.FileData = fileData
    # Just for visualization purposes
    def printString(self):
        outputString = '{0}: {1}'.format('Filename', self.FileName)
        outputString+='\n'
        for key,value in self.FileData.items():
            outputString+='{0} {1} {2} {3}'.format(key, ':', value, '\t')
        outputString+='\n'
        return outputString


