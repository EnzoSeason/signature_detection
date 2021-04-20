from typing import Any
import numpy as np


class Judger:
    """
    read the cropped mask and identify if it's a signature

    Attributes:
    -----------
    - size_ratio: [low, high]

        low < max(h, w) / min(h, w) < high.

        h, w are the heigth and width of the input mask.

    - max_pixel_ratio: [low, high]

       low < the number of 0 / the number of 255 < high.

       The mask should only have 2 value, 0 and 255.

    Methods:
    --------
    - judge(mask: numpy array) -> bool

       identify if the mask is a signature
    """

    def __init__(self, size_ratio=[1, 4], pixel_ratio=[0.01, 1]) -> None:
        self.size_ratio = size_ratio
        self.pixel_ratio = pixel_ratio

    def __str__(self) -> str:
        s = "\nJudger\n==========\n"
        s += "size_ratio = {}\n".format(str(self.size_ratio))
        s += "pixel_ratio = {}\n".format(str(self.pixel_ratio))
        return s

    def _is_valid_mask(self, mask: Any) -> bool:
        values = np.unique(mask)
        if len(values) != 2:
            return False
        if values[0] != 0 or values[1] != 255:
            return False
        return True

    def judge(self, mask: Any) -> bool:
        if self._is_valid_mask(mask):
            size_ratio = max(mask.shape) / min(mask.shape)
            if size_ratio < self.size_ratio[0] or size_ratio > self.size_ratio[1]:
                return False

            bincounts = np.bincount(mask.ravel())
            pixel_ratio = bincounts[0] / bincounts[255]
            if pixel_ratio < self.pixel_ratio[0] or pixel_ratio > self.pixel_ratio[1]:
                return False

            return True
        else:
            return False

    def run(self, results: dict) -> list:
        regions = []
        for idx, result in results.items():
            is_signed = self.judge(result["cropped_mask"])
            regions.append({"id": idx, "signed": is_signed, "box": result["cropped_region"]})
        return regions
