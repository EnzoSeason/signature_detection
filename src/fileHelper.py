import os


class FileHelper:
    @staticmethod
    def getFileExtenstion(fileName) -> str:
        basename = os.path.basename(fileName)
        dn, dext = os.path.splitext(basename)
        return dext[1:]