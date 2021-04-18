import math
from typing import Any
import cv2
import numpy as np
from PIL import Image


class Cropper:
    """
    read the mask extracted by Extractor, and crop it.

    Attributes:
    -----------
      - min_region_size

        the min area size of the signature.

        - border_ratio: float

            border = min(h, w) * border_ratio

            h, w are the heigth and width of the input mask.
            The border will be removed by the function _remove_borders.

    Methods:
    --------
      - find_contours(img: numpy array) -> sorted_boxes: numpy array

        find the contours and sort them by area size

      - is_intersected(box_a: [x, y, w, h], box_b: [x, y, w, h]) -> bool

        check box_a and box_b is intersected

      - merge_boxes(box_a: [x, y, w, h], box_b: [x, y, w, h]) -> [x, y, w, h]:

        merge the intersected boxes into one

      - boxes2regions(sorted_boxes) -> dict:

        transform all the sorted_boxes into regions (merged boxes)

      - crop_regions(img: numpy array, regions: dict) -> list:

        return a list of cropped images (np.array)

      - run(img_path) -> list

        main function, crop the signatures,
        return a list of cropped images (np.array)
    """

    def __init__(self, min_region_size=10000, border_ratio=0.1):
        self.min_region_size = min_region_size
        self.border_ratio = border_ratio

    def __str__(self) -> str:
        s = "\nCropper\n==========\n"
        s += "min_region_size = {}\n".format(self.min_region_size)
        s += "border_ratio = {}\n".format(self.border_ratio)
        return s

    def find_contours(self, img):
        """
        find contours limited by min_region_size
        in the binary image.

        The contours are sorted by area size, from large to small.

        Params:
          img: numpy array
        Return:
          boxes: A numpy array of contours.
          each items in the array is a contour (x, y, w, h)
        """
        cnts = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt = cnts[0] if len(cnts) == 2 else cnts[1]

        boxes = []
        copy_img = img.copy()
        for c in cnt:
            (x, y, w, h) = cv2.boundingRect(c)

            if (
                h * w > self.min_region_size
                and h < copy_img.shape[0]
                and w < copy_img.shape[1]
            ):

                # cv2.rectangle(copy_img, (x, y), (x + w, y + h), (155, 155, 0), 1)
                boxes.append([x, y, w, h])

        np_boxes = np.array(boxes)
        # sort the boxes by area size
        area_size = list(map(lambda box: box[2] * box[3], np_boxes))
        area_size = np.array(area_size)
        area_dec_order = area_size.argsort()[::-1]
        sorted_boxes = np_boxes[area_dec_order]

        return sorted_boxes

    def is_intersected(self, new_box, orignal_box) -> bool:
        [x_a, y_a, w_a, h_a] = new_box
        [x_b, y_b, w_b, h_b] = orignal_box

        if y_a > y_b + h_b:
            return False
        if y_a + h_a < y_b:
            return False
        if x_a > x_b + w_b:
            return False
        if x_a + w_a < x_b:
            return False
        return True

    def merge_boxes(self, box_a, box_b) -> list:
        """
        merge 2 intersected box into one
        """
        [x_a, y_a, w_a, h_a] = box_a
        [x_b, y_b, w_b, h_b] = box_b

        min_x = min(x_a, x_b)
        min_y = min(y_a, y_b)
        max_w = max(w_a, w_b, (x_b + w_b - x_a), (x_a + w_a - x_b))
        max_h = max(h_a, h_b, (y_b + h_b - y_a), (y_a + h_a - y_b))

        return [min_x, min_y, max_w, max_h]

    def _remove_borders(self, box) -> Any:
        """
        remove the borders around the box
        """
        [x, y, w, h] = box
        border = math.floor(min(w, h) * self.border_ratio)
        return [x + border, y + border, w - border, h - border]

    def boxes2regions(self, sorted_boxes) -> dict:
        regions = {}

        for box in sorted_boxes:
            if len(regions) == 0:
                regions[0] = box
            else:
                is_merged = False
                for key, region in regions.items():
                    if self.is_intersected(box, region) == True:
                        new_region = self.merge_boxes(region, box)
                        regions[key] = new_region
                        is_merged = True
                        break
                if is_merged == False:
                    key = len(regions)
                    regions[key] = box

        return regions

    def crop_regions(self, mask, regions) -> dict:
        results = {}
        for key, region in regions.items():
            # crop region
            cropped_region = self._remove_borders(region)
            [x, y, w, h] = cropped_region

            image = Image.fromarray(mask)
            cropped_image = image.crop((x, y, x + w, y + h))
            cropped_mask = np.array(cropped_image)

            results[key] = {
                "cropped_region": cropped_region,
                "cropped_mask": cropped_mask,
            }

        return results

    def run(self, np_image):
        """
        read the signature extracted by Extractor, and crop it.
        """

        # find contours
        sorted_boxes = self.find_contours(np_image)

        # get regions
        regions = self.boxes2regions(sorted_boxes)

        # crop regions
        return self.crop_regions(np_image, regions)
