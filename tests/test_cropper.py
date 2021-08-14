import sys
import unittest

import numpy as np

sys.path.append("..")

from signature_detect.cropper import Cropper
from signature_detect.extractor import Extractor
from signature_detect.loader import Loader

from tests.data.dummy import TEST_IMAGE_PATH


class TestCropper(unittest.TestCase):
    def test_init(self):
        cropper = Cropper()
        self.assertEqual(cropper.min_region_size, 10000)

    def test_str(self):
        cropper = Cropper()
        s = "\nCropper\n==========\n"
        s += "min_region_size = {}\n".format(cropper.min_region_size)
        s += "border_ratio = {}\n".format(cropper.border_ratio)
        self.assertEqual(str(cropper), s)

    def test_run(self):
        path = TEST_IMAGE_PATH

        loader = Loader()
        mask = loader.get_masks(path)[0]

        extractor = Extractor()
        labeled_mask = extractor.extract(mask)

        cropper = Cropper()
        results = cropper.run(labeled_mask)
        self.assertEqual(len(results[0]["cropped_region"]), 4)

        mask_list = list(np.unique(results[0]["cropped_mask"]))
        self.assertEqual(mask_list[0], 0)
        self.assertEqual(mask_list[1], 255)

    def test_boxes2regions(self):
        cropper = Cropper(border_ratio=0)
        boxes = [[0, 0, 10, 10], [9, 9, 5, 5], [20, 20, 1, 1]]
        regions = cropper.boxes2regions(boxes)
        self.assertEqual(len(regions), 2)

        self.assertEqual(regions[0][0], 0)
        self.assertEqual(regions[0][1], 0)
        self.assertEqual(regions[0][2], 14)
        self.assertEqual(regions[0][3], 14)

        self.assertEqual(regions[1][0], 20)
        self.assertEqual(regions[1][1], 20)
        self.assertEqual(regions[1][2], 1)
        self.assertEqual(regions[1][2], 1)

    def test_is_intersected(self):
        cropper = Cropper()
        box_b = [10, 10, 1, 1]

        # y_a > y_b + h_b
        box_a = [0, 20, 1, 1]
        self.assertFalse(cropper.is_intersected(box_a, box_b))

        # y_a + h_a < y_b
        box_a = [0, 0, 1, 1]
        self.assertFalse(cropper.is_intersected(box_a, box_b))

        # x_a > x_b + w_b
        box_a = [20, 10, 1, 1]
        self.assertFalse(cropper.is_intersected(box_a, box_b))

        # x_a + w_a < x_b
        box_a = [0, 10, 1, 1]
        self.assertFalse(cropper.is_intersected(box_a, box_b))
