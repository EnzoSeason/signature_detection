import sys
import unittest

import numpy as np

sys.path.append("..")

from src.cropper import Cropper
from src.extractor import Extractor
from src.loader import Loader

from tests.data.dummy import TEST_IMAGE_PATH


class TestCropper(unittest.TestCase):
    def test_init(self):
        cropper = Cropper()
        self.assertEqual(cropper.min_region_size, 10000)

    def test_str(self):
        cropper = Cropper()
        s = "\nCropper\n==========\n"
        s += "min_region_size = {}\n".format(cropper.min_region_size)
        self.assertEqual(str(cropper), s)

    def test_run(self):
        path = TEST_IMAGE_PATH

        loader = Loader()
        mask = loader.get_masks(path)[0]

        extractor = Extractor()
        labeled_mask = extractor.extract(mask)

        cropper = Cropper()
        cropped_images = cropper.run(labeled_mask)
        self.assertEqual(len(cropped_images), 1)

        mask_list = list(np.unique(cropped_images[0]))
        self.assertEqual(mask_list[0], 0)
        self.assertEqual(mask_list[1], 255)

    def test_boxes2regions(self):
        cropper = Cropper()
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
        box_a = [10, 10, 1, 1]

        box_b = [0, 0, 1, 1]
        self.assertFalse(cropper.is_intersected(box_a, box_b))

        box_b = [0, 10, 1, 1]
        self.assertFalse(cropper.is_intersected(box_a, box_b))

        box_b = [20, 10, 1, 1]
        self.assertFalse(cropper.is_intersected(box_a, box_b))

