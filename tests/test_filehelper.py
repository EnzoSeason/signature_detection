import unittest
import sys

sys.path.append("..")

from src.filehelper import FileHelper


class TestFilehelper(unittest.TestCase):
    def test_getFileExtenstion(self):
        file = "test.txt"
        ext = FileHelper.getFileExtenstion(file)
        self.assertEqual(ext, "txt")
