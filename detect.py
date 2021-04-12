import csv
import os

from src.loader import Loader
from src.extractor import Extractor
from src.cropper import Cropper
from src.judger import Judger

def main():
    # load files
    files = os.listdir("./private/files")
    n_files = len(files)
    files_idxs = list(range(1, 31))
    # init workers
    loader = Loader()
    extractor = Extractor()
    cropper = Cropper()
    judger = Judger()
    # detect
    file_name = "./private/results.csv"
    with open(file_name, "w") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=["id", "signed"], delimiter=","
        )
        writer.writeheader()
    with open(file_name, "a") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["id", "signed"], delimiter=",")
        for file in files_idxs:
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