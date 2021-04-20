from typing import Any
from skimage import measure, morphology
from skimage.measure import regionprops
import numpy as np


class Extractor:
    """
    Extract the signature from a mask. The process is as followed.

    1. It finds the regions in an image mask. Each region has a label (unique number).
    2. It removes the small regions. The small region is defined by attributes.
    3. It remove the big regions. The big region is defined by attributes.
    4. It returns a labeled image. The numbers in the image are the region labels, NOT pixels.

    Attributes
    ----------
    outlier_weight: int
        The weight of small outlier size
    outlier_bias: int
        The bias of small outlier size
    amplfier: int
        The amplfier calculates the big outlier size from the small one
    min_area_size: int
        The min region area size in the labeled image.

    Methods
    -------
    extract(mask: numpy.array):
        extract the signature
    """

    def __init__(
        self, outlier_weight=3, outlier_bias=100, amplfier=10, min_area_size=10
    ):
        # the parameters are used to remove small size connected pixels outlier
        self.outlier_weight = outlier_weight
        self.outlier_bias = outlier_bias
        # the parameter is used to remove big size connected pixels outlier
        self.amplfier = amplfier
        self.min_area_size = min_area_size

    def __str__(self) -> str:
        s = "\nExtractor\n==========\n"
        s += "outlier_weight = {}\n".format(self.outlier_weight)
        s += "outlier_bias = {}\n".format(self.outlier_bias)
        s += "> small_outlier_size = outlier_weight * average_region_size + outlier_bias\n"
        s += "amplfier = {}\n".format(self.amplfier)
        s += "> large_outlier_size = amplfier * small_outlier_size\n"
        s += "min_area_size = {} (pixels)\n".format(self.min_area_size)
        s += "> min_area_size is used to calculate average_region_size.\n"
        return s

    def extract(self, mask) -> Any:
        """
        params
        ------
        mask: numpy array
            The mask of the image. It's calculated by Loader.

        return
        ------
        labeled_image: numpy array
            The labeled image.
            The numbers in the array are the region labels.
        """
        condition = mask > mask.mean()
        labels = measure.label(condition, background=1)

        total_pixels = 0
        nb_region = 0
        average = 0.0
        for region in regionprops(labels):
            if region.area > self.min_area_size:
                total_pixels += region.area
                nb_region += 1
        
        if nb_region > 1:
            average = total_pixels / nb_region
            # small_size_outlier is used as a threshold value to remove pixels
            # are smaller than small_size_outlier
            small_size_outlier = average * self.outlier_weight + self.outlier_bias

            # big_size_outlier is used as a threshold value to remove pixels
            # are bigger than big_size_outlier
            big_size_outlier = small_size_outlier * self.amplfier

            # remove small pixels
            labeled_image = morphology.remove_small_objects(labels, small_size_outlier)
            # remove the big pixels
            component_sizes = np.bincount(labeled_image.ravel())
            too_small = component_sizes > (big_size_outlier)
            too_small_mask = too_small[labeled_image]
            labeled_image[too_small_mask] = 0

            labeled_mask = np.full(labeled_image.shape, 255, dtype="uint8")
            labeled_mask = labeled_mask * (labeled_image == 0)
        else:
            labeled_mask = mask

        return labeled_mask
