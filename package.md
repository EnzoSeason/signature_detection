# Signature Detection

A simple tool to detect if there are **signatures** in **an image** or **a PDF file**.

The full documentation is presented at the [Github Repository](https://github.com/EnzoSeason/signature_detection).

## Extra Dependencies

This tool uses `Wand` to convert a PDF file into images. 

`Wand` is a ctypes-based simple `ImageMagick` binding for Python. You may need to install `ImageMagick` on your local machine.

More details are available [here](https://docs.wand-py.org/en/0.6.6/).

## Usage

Signature_detect contains 4 classes.

1. Loader
2. Extractor
3. Cropper
4. Judger

### Loader

Loader can read an image or a PDF file page by page.

It returns a list of the masks. Each mask is a numpy 2 dimensions array. Its element's value is `0` or `255`.

```python
from signature_detect.loader import Loader

loader = Loader(
    low_threshold=(0, 0, 250), 
    high_threshold=(255, 255, 255))

masks = loader.get_masks(file_path)
```


### Extractor

Extractor reads a mask, labels the regions in the mask, and removes both small and big regions. We consider that the signature is a region of middle size.

```python
from signature_detect.extractor import Extractor

extractor = Extractor(
    outlier_weight=3, 
    outlier_bias=100, 
    amplfier=10, 
    min_area_size=10)

labeled_mask = extractor.extract(mask)
```

### Cropper

Cropper crops the regions in the labeled mask.

```python
from signature_detect.cropper import Cropper

cropper = Cropper(
    min_region_size=10000, 
    border_ratio=0.1)

results = cropper.run(labeled_mask)
```

### Judger

Judger decides whether a region is a signature.

```python
from signature_detect.judger import Judger

judger = Judger(
    size_ratio=[1, 4], 
    pixel_ratio=[0.01, 1])

is_signed = judger.judge(result["cropped_mask"])
```

## Dev version

If you would like to develop this package and run the tests, you can download the code and install dev environment locally.

```bash
pip install -e .[dev]
```