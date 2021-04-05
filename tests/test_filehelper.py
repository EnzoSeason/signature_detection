import unittest
import sys
sys.path.append('..')

from src.filehelper import FileHelper


class TestFilehelper(unittest.TestCase):
    def test_getFileExtenstion(self):
        file = "test.txt"
        ext = FileHelper.getFileExtenstion(file)
        self.assertEqual(ext, 'txt')
    
    def test_fileToImages(self):
        file = "./data/signed_file.pdf"
        images = FileHelper.fileToImages(file)
        self.assertEqual(len(images), 2)