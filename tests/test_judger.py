import sys
import unittest

import numpy as np

sys.path.append("..")

from src.judger import Judger


class TestJudger(unittest.TestCase):
    def test_init(self):
        judger = Judger()
        self.assertEqual(judger.size_ratio, 4)
        self.assertEqual(judger.pixel_ratio, 0.5)

    def test_str(self):
        judger = Judger()
        s = "\nJudger\n==========\n"
        s += "size_ratio = {}\n".format(judger.size_ratio)
        s += "pixel_ratio = {}\n".format(judger.pixel_ratio)
        self.assertEqual(str(judger), s)

    def test_is_valid_mask(self):
        judger = Judger()

        mask = np.array([0])
        with self.assertRaises(Exception) as cm:
            judger._is_valid_mask(mask)
        self.assertEqual(
            cm.exception.__str__(), "The input np.array should have 2 value."
        )

        mask = np.array([0, 1])
        with self.assertRaises(Exception) as cm:
            judger._is_valid_mask(mask)
        self.assertEqual(
            cm.exception.__str__(),
            "The input np.array should only have 2 value, 0 and 255.",
        )

        mask = np.array([0, 255])
        res = judger._is_valid_mask(mask)
        self.assertTrue(res)
    
    def test_judge(self):
        judger = Judger()

        mask = np.array([[255,0,0,0,0]])
        res = judger.judge(mask)
        self.assertFalse(res)

        mask = np.array([[255], [0]])
        res = judger.judge(mask)
        self.assertFalse(res)

        mask = np.array([[255, 255, 255], [0, 255, 255]])
        res = judger.judge(mask)
        self.assertTrue(res)
