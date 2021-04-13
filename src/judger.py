from typing import Any
import math
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

    def __init__(
        self, size_ratio=[1, 4], pixel_ratio=[0.01, 1], border_ratio=0.1
    ) -> None:
        self.size_ratio = size_ratio
        self.pixel_ratio = pixel_ratio
        self.border_ratio = border_ratio

    def __str__(self) -> str:
        s = "\nJudger\n==========\n"
        s += "size_ratio = {}\n".format(str(self.size_ratio))
        s += "pixel_ratio = {}\n".format(str(self.pixel_ratio))
        s += "border_ratio = {}\n".format(str(self.border_ratio))
        return s

    def _is_valid_mask(self, mask: Any) -> bool:
        values = np.unique(mask)
        if len(values) != 2:
            raise Exception("The input np.array should have 2 value.")
        if values[0] != 0 or values[1] != 255:
            raise Exception("The input np.array should only have 2 value, 0 and 255.")
        return True

    def _remove_borders(self, mask: Any) -> Any:
        """
        remove the borders around the mask
        """
        border = math.floor(min(mask.shape) * self.border_ratio)
        return mask[border : mask.shape[0] - border, border : mask.shape[1] - border]

    def judge(self, mask: Any) -> bool:
        if self._is_valid_mask(mask):
            mask = self._remove_borders(mask)
            size_ratio = max(mask.shape) / min(mask.shape)
            if size_ratio < self.size_ratio[0] or size_ratio > self.size_ratio[1]:
                return False

            bincounts = np.bincount(mask.ravel())
            pixel_ratio = bincounts[0] / bincounts[255]
            if pixel_ratio < self.pixel_ratio[0] or pixel_ratio > self.pixel_ratio[1]:
                return False

            return True