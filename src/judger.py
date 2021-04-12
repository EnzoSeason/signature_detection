from typing import Any

import numpy as np


class Judger:
    """
    read the cropped mask and identify if it's a signature

    Attributes:
    -----------
    - size_ratio: int

        It's max(h, w) / min(h, w).

        h, w are the heigth and width of the input mask.
    - max_pixel_ratio: int

       It's the number of 0 / the number of 255 in the mask.

       The mask should only have 2 value, 0 and 255.

    Methods:
    --------
    - judge(mask: numpy array) -> bool

       identify if the mask is a signature
    """

    def __init__(self, size_ratio=4, min_pixel_ratio=0.1, max_pixel_ratio=1) -> None:
        self.size_ratio = size_ratio
        self.min_pixel_ratio = min_pixel_ratio
        self.max_pixel_ratio = max_pixel_ratio

    def __str__(self) -> str:
        s = "\nJudger\n==========\n"
        s += "size_ratio = {}\n".format(self.size_ratio)
        s += "min_pixel_ratio = {}\n".format(self.min_pixel_ratio)
        s += "max_pixel_ratio = {}\n".format(self.max_pixel_ratio)
        return s

    def _is_valid_mask(self, mask: Any) -> bool:
        values = np.unique(mask)
        if len(values) != 2:
            raise Exception("The input np.array should have 2 value.")
        if values[0] != 0 or values[1] != 255:
            raise Exception("The input np.array should only have 2 value, 0 and 255.")
        return True

    def judge(self, mask: Any) -> bool:
        if self._is_valid_mask(mask):
            if max(mask.shape) / min(mask.shape) > self.size_ratio:
                return False

            bincounts = np.bincount(mask.ravel())
            print(bincounts[0] / bincounts[255])
            if (
                bincounts[0] / bincounts[255] > self.max_pixel_ratio
                or bincounts[0] / bincounts[255] < self.min_pixel_ratio
            ):
                return False

            return True