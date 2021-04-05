import unittest
import sys
sys.path.append('..')

from src.loader import Loader
from src.extractor import Extractor

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
        path = "./data/signed_image.jpg"
        loader = Loader()
        mask = loader.get_masks(path)[0]

        extractor = Extractor()
        labeled_mask = extractor.extract(mask)
        self.assertTrue(len(labeled_mask))
