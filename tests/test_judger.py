import sys
import unittest

import numpy as np

sys.path.append("..")

from signature_detect.cropper import Cropper
from signature_detect.extractor import Extractor
from signature_detect.loader import Loader
from signature_detect.judger import Judger

from tests.data.dummy import TEST_IMAGE_PATH

class TestJudger(unittest.TestCase):
    def test_init(self):
        judger = Judger()
        self.assertEqual(judger.size_ratio[0], 1)
        self.assertEqual(judger.size_ratio[1], 4)
        self.assertEqual(judger.pixel_ratio[0], 0.01)
        self.assertEqual(judger.pixel_ratio[1], 1)

    def test_str(self):
        judger = Judger()
        s = "\nJudger\n==========\n"
        s += "size_ratio = {}\n".format(judger.size_ratio)
        s += "pixel_ratio = {}\n".format(judger.pixel_ratio)
        self.assertEqual(str(judger), s)

    def test_is_valid_mask(self):
        judger = Judger()

        mask = np.array([[0,0,0,0]])
        res = judger.judge(mask)
        self.assertFalse(res)

        mask = np.array([0])
        self.assertFalse(judger._is_valid_mask(mask))

        mask = np.array([0, 1])
        self.assertFalse(judger._is_valid_mask(mask))

        mask = np.array([0, 255])
        res = judger._is_valid_mask(mask)
        self.assertTrue(res)
    
    def test_judge(self):
        judger = Judger()

        mask = np.array([[255,0,0,0,0]])
        res = judger.judge(mask)
        self.assertFalse(res)

        mask = np.array([[255, 0], [0, 0]])
        res = judger.judge(mask)
        self.assertFalse(res)

        mask = np.array([[255, 255, 255], [0, 255, 255]])
        res = judger.judge(mask)
        self.assertTrue(res)
    
    def test_run(self):
        path = TEST_IMAGE_PATH

        loader = Loader()
        mask = loader.get_masks(path)[0]

        extractor = Extractor()
        labeled_mask = extractor.extract(mask)

        cropper = Cropper()
        results = cropper.run(labeled_mask)

        judger = Judger()
        regions = judger.run(results)
        
        # assert
        region = regions[0]
        self.assertEqual(region["id"], 0)
        self.assertEqual(region["signed"], True)
        comparison = region["box"] == results[0]["cropped_region"]
        self.assertTrue(comparison.all())
