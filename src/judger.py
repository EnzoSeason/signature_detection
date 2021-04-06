from typing import Any

import numpy as np


class Judger:
    '''
    read the cropped mask and identify if it's a signature

    Attributes:
    -----------
    - size_ratio: int
      
        It's max(h, w) / min(h, w). 
        
        h, w are the heigth and width of the input mask.
    - pixel_ratio: int
       
       It's the number of 0 / the number of 255 in the mask.
       
       The mask should only have 2 value, 0 and 255.
    
    Methods:
    --------
    - judge(mask: numpy array) -> bool
       
       identify if the mask is a signature
    '''
    def __init__(self, size_ratio=4, pixel_ratio=0.5) -> None:
        self.size_ratio = size_ratio
        self.pixel_ratio = pixel_ratio

    def __str__(self) -> str:
        s = "\nJudger\n==========\n"
        s += "size_ratio = {}\n".format(self.size_ratio)
        s += "pixel_ratio = {}\n".format(self.pixel_ratio)
        return s
    
    def _is_valid_mask(self, mask: Any) -> bool:
        values = np.unique(mask)
        if len(values) != 2:
            raise Exception('The input np.array should have 2 value.')
        if values[0] != 0 or values[1] != 255:
            raise Exception('The input np.array should only have 2 value, 0 and 255.')
        return True
    
    def judge(self, mask: Any) -> bool:
        if self._is_valid_mask(mask):
            if max(mask.shape) / min(mask.shape) > self.size_ratio:
                return False
            
            bincounts = np.bincount(mask.ravel())
            if bincounts[0] / bincounts[255] > self.pixel_ratio:
                return False
            
            return True