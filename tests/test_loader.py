import unittest
import sys
from unittest import loader

sys.path.append("..")

from src.loader import Loader


class TestLoader(unittest.TestCase):
    def test_loader_init(self):
        loader = Loader()
        self.assertEqual(loader.low_threshold, (0, 0, 250))

    def test_is_valid(self):
        low_threshold = ""
        with self.assertRaises(Exception) as cm:
            Loader(low_threshold)
        self.assertEqual(cm.exception.__str__(), "The threshold must be a tuple.")

        low_threshold = (0, 1)
        with self.assertRaises(Exception) as cm:
            Loader(low_threshold)
        self.assertEqual(cm.exception.__str__(), "The threshold must have 3 item (h, s, v).")

        low_threshold = (0, 0, 256)
        with self.assertRaises(Exception) as cm:
            Loader(low_threshold)
        self.assertEqual(cm.exception.__str__(), "The threshold item must be in the range [0, 255].")
        
        low_threshold = (0, 0, '0')
        with self.assertRaises(Exception) as cm:
            Loader(low_threshold)
        self.assertEqual(cm.exception.__str__(), "The threshold item must be in the range [0, 255].")
    
    def test_get_masks(self):
        path = "./data/test.txt"
        loader = Loader()
        with self.assertRaises(Exception) as cm:
            loader.get_masks(path)
        self.assertEqual(cm.exception.__str__(), "Document should be jpg/jpeg, png or pdf.")

        path = "./data/signed_image.jpeg"
        masks = loader.get_masks(path)
        self.assertEqual(len(masks), 1)

        path = "./data/signed_file.pdf"
        masks = loader.get_masks(path)
        self.assertEqual(len(masks), 2)


