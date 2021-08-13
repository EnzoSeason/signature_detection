from signature_detect.loader import Loader
from signature_detect.cropper import Cropper
from signature_detect.extractor import Extractor
from signature_detect.bounding_box import Bounding_box

path = 'check_bbox/aam09c00.tif'

# Loader
loader = Loader()
mask = loader.get_masks(path)[0]

# Extractor
extractor = Extractor(amplfier=15)
labeled_mask = extractor.extract(mask)

# Cropper
cropper = Cropper()
results = cropper.run(labeled_mask)

# Bbox
check = Bounding_box().run(labeled_mask)
print(check)
# check value = [1024, 1443, 546, 96]
