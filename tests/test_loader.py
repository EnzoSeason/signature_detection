import sys
import unittest

import numpy as np

sys.path.append("..")

from signature_detect.loader import Loader

from tests.data.dummy import TEST_IMAGE_PATH, TEST_PDF_PATH, TEST_TIF_PATH


class TestLoader(unittest.TestCase):
    def test_loader_init(self):
        loader = Loader()
        self.assertEqual(loader.low_threshold, (0, 0, 250))

    def test_str(self):
        loader = Loader()
        s = "\nLoader\n==========\n"
        s += "low_threshold = {}\n".format(loader.low_threshold)
        s += "high_threshold = {}\n".format(loader.high_threshold)
        self.assertEqual(str(loader), s)

    def test_is_valid(self):
        low_threshold = ""
        with self.assertRaises(Exception) as cm:
            Loader(low_threshold)
        self.assertEqual(cm.exception.__str__(), "The threshold must be a tuple.")

        low_threshold = (0, 1)
        with self.assertRaises(Exception) as cm:
            Loader(low_threshold)
        self.assertEqual(
            cm.exception.__str__(), "The threshold must have 3 item (h, s, v)."
        )

        low_threshold = (0, 0, 256)
        with self.assertRaises(Exception) as cm:
            Loader(low_threshold)
        self.assertEqual(
            cm.exception.__str__(), "The threshold item must be in the range [0, 255]."
        )

        low_threshold = (0, 0, "0")
        with self.assertRaises(Exception) as cm:
            Loader(low_threshold)
        self.assertEqual(
            cm.exception.__str__(), "The threshold item must be in the range [0, 255]."
        )

    def test_get_masks(self):
        path = "./data/test.txt"
        loader = Loader()
        with self.assertRaises(Exception) as cm:
            loader.get_masks(path)
        self.assertEqual(
            cm.exception.__str__(), "Document should be jpg/jpeg, png, tif or pdf."
        )

        # jpeg test
        path = TEST_IMAGE_PATH
        masks = loader.get_masks(path)
        self.assertEqual(len(masks), 1)

        first_mask_list = list(np.unique(masks[0]))
        self.assertEqual(first_mask_list[0], 0)
        self.assertEqual(first_mask_list[1], 255)

        # tif test
        path = TEST_TIF_PATH
        masks = loader.get_masks(path)
        self.assertEqual(len(masks), 1)

        first_mask_list = list(np.unique(masks[0]))
        self.assertEqual(first_mask_list[0], 0)
        self.assertEqual(first_mask_list[1], 255)

        # pdf test
        path = TEST_PDF_PATH
        masks = loader.get_masks(path)
        self.assertEqual(len(masks), 2)

        mask_list = list(np.unique(masks[1]))
        self.assertEqual(mask_list[0], 0)
        self.assertEqual(mask_list[1], 255)
