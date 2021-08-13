from signature_detect.loader import Loader
from signature_detect.cropper import Cropper
from signature_detect.extractor import Extractor
from signature_detect.bounding_box import Bounding_box
import cv2

path = '/Users/veersingh/Desktop/docs_with_signs_dataset(tobacco800)/images/aam09c00.tif'


image = cv2.imread(path)

# Loader
loader = Loader()
mask = loader.get_masks(path)[0]

# Extractor
extractor = Extractor(amplfier=15)
labeled_mask = extractor.extract(mask)

# Cropper
cropper = Cropper()
results = cropper.run(labeled_mask)

# bbox
check = Bounding_box().run(labeled_mask)
print(check)
# check value = [1024, 1443, 546, 96]
