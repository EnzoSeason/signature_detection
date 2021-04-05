import os
from typing import Any

from pdf2image import convert_from_bytes


class FileHelper:
    @staticmethod
    def getFileExtenstion(fileName) -> str:
        basename = os.path.basename(fileName)
        dn, dext = os.path.splitext(basename)
        return dext[1:]

    @staticmethod
    def fileToImages(file_name) -> Any:
        with open(file_name, "rb") as file:
            pdf_test = file.read()
            images = convert_from_bytes(pdf_test)
            return images