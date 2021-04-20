import sys
import unittest

import numpy as np

sys.path.append("..")

from signature_detect.extractor import Extractor
from signature_detect.loader import Loader

from tests.data.dummy import TEST_IMAGE_PATH


class TestExtractor(unittest.TestCase):
    def test_init(self):
        extractor = Extractor()
        self.assertEqual(extractor.outlier_weight, 3)
        self.assertEqual(extractor.outlier_bias, 100)
        self.assertEqual(extractor.amplfier, 10)
        self.assertEqual(extractor.min_area_size, 10)

    def test_str(self):
        extractor = Extractor()
        s = "\nExtractor\n==========\n"
        s += "outlier_weight = 3\n"
        s += "outlier_bias = 100\n"
        s += "> small_outlier_size = outlier_weight * average_region_size + outlier_bias\n"
        s += "amplfier = 10\n"
        s += "> large_outlier_size = amplfier * small_outlier_size\n"
        s += "min_area_size = 10 (pixels)\n"
        s += "> min_area_size is used to calculate average_region_size.\n"
        self.assertEqual(str(extractor), s)

    def test_extract(self):
        path = TEST_IMAGE_PATH
        loader = Loader()
        mask = loader.get_masks(path)[0]

        extractor = Extractor()
        labeled_mask = extractor.extract(mask)
        mask_list = list(np.unique(labeled_mask))
        self.assertEqual(mask_list[0], 0)
        self.assertEqual(mask_list[1], 255)

        mask = np.array([[0, 255, 0], [0, 255, 0]], dtype="uint8")
        labeled_mask = extractor.extract(mask)

        mask_bincounts = list(np.bincount(mask.ravel()))
        labeled_mask_bincounts = list(np.bincount(labeled_mask.ravel()))
        self.assertEqual(mask_bincounts[0], labeled_mask_bincounts[0])
        self.assertEqual(mask_bincounts[255], labeled_mask_bincounts[255])
