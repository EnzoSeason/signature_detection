import csv
import os
import random
from typing import List

from src.loader import Loader
from src.extractor import Extractor
from src.cropper import Cropper
from src.judger import Judger


def partition(l: List[int], n: int):
    copied_l = l
    random.shuffle(copied_l)
    return [copied_l[i::n] for i in range(n)]


def main():
    # load files
    files = os.listdir("./private/files")
    n_files = len(files)
    files_idxs = list(range(1, n_files+1))
    #  hyper params
    amplfiers = [5, 10, 15]
    min_region_sizes = [5000, 10000, 20000]
    size_ratios = [3, 4, 5]
    pixel_ratios = [0.25, 0.5, 1]
    # split files
    n = len(amplfiers) * len(min_region_sizes) * len(size_ratios) * len(pixel_ratios)
    data = partition(files_idxs, n)
    # Tuning
    loader = Loader()
    for i, files in enumerate(data):
        pixel_ratio_idx = i % len(pixel_ratios)
        size_ratio_idx = (i // len(pixel_ratios)) % len(size_ratios)
        min_region_size_idx = (i // (len(pixel_ratios) * len(size_ratios))) % len(
            min_region_sizes
        )
        amplfier_idx = (
            i // (len(pixel_ratios) * len(size_ratios) * len(min_region_sizes))
        ) % len(amplfiers)

        extractor = Extractor(amplfier=amplfiers[amplfier_idx])
        cropper = Cropper(min_region_size=min_region_sizes[min_region_size_idx])
        judger = Judger(
            size_ratio=size_ratios[size_ratio_idx],
            pixel_ratio=pixel_ratios[pixel_ratio_idx],
        )

        for file in files:
            file_name = "./private/tuning/amplfier_{}_min_region_size_{}_size_ratio_{}_pixel_ratio_{}.csv".format(
                amplfiers[amplfier_idx],
                min_region_sizes[min_region_size_idx],
                size_ratios[size_ratio_idx],
                pixel_ratios[pixel_ratio_idx],
            )
            with open(file_name, "w") as csvfile:
                writer = csv.DictWriter(
                    csvfile, fieldnames=["id", "signed"], delimiter=","
                )
                writer.writeheader()
            with open(file_name, "a") as csvfile:
                writer = csv.DictWriter(
                    csvfile, fieldnames=["id", "signed"], delimiter=","
                )
                try:
                    masks = loader.get_masks("./private/files/" + str(file) + ".pdf")
                    is_signed = False
                    for mask in masks:
                        labeled_mask = extractor.extract(mask)
                        cropped_images = cropper.run(labeled_mask)
                        for cropped_image in cropped_images:
                            is_signed = judger.judge(cropped_image)
                            if is_signed:
                                break
                        if is_signed:
                            break
                    row = {}
                    row["id"] = file
                    row["signed"] = 1 if is_signed else 0
                    print(row)
                    writer.writerow(row)
                except Exception as e:
                    print(e)
                    continue


if __name__ == "__main__":
    main()