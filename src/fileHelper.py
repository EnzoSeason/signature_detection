import csv
import io
import os

from pdf2image import convert_from_bytes


class FileHelper:
    @staticmethod
    def getFileNameAndExtension(filePath):
        basename = os.path.basename(filePath)
        dn, dext = os.path.splitext(basename)
        return dn, dext[1:]

    @staticmethod
    def getFileExtenstion(fileName):
        basename = os.path.basename(fileName)
        dn, dext = os.path.splitext(basename)
        return dext[1:]

    @staticmethod
    def fileToImages(file_name):
        with open(file_name, 'rb') as file:
            pdf_test = file.read()
            images = convert_from_bytes(pdf_test)
            return images

    @staticmethod
    def imagesToBytes(images):
        bytes_array = []
        for i in range(len(images)):
            img_byte_arr = io.BytesIO()
            images[i].save(img_byte_arr, format='PNG')
            bytes_array.append(img_byte_arr.getvalue())
        return bytes_array