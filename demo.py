import sys


from src.loader import Loader
from src.extractor import Extractor
from src.cropper import Cropper
from src.judger import Judger


def main(file_path: str) -> None:
    loader = Loader()
    extractor = Extractor(amplfier=15)
    cropper = Cropper()
    judger = Judger()

    try:
        masks = loader.get_masks(file_path)
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
        print(is_signed)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    file_path = None
    for i in range(len(sys.argv)):
        if sys.argv[i] == "--file":
            file_path = sys.argv[i + 1]
    if file_path is None:
        print("Need input file")
        print("python demo.py --file my-file.pdf")
    else:
        main(file_path)
