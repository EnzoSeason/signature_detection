from setuptools import setup

with open("package.md", "r") as md:
    long_description = md.read()

setup(
    name="signature-detect",
    version="0.1.4",
    url="https://github.com/EnzoSeason/signature_detection",
    author="Jijie LIU",
    author_email="liujijieseason@gmail.com",
    description="A package for the signature detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=[
        "signature_detect",
    ],
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.0",
        "pillow>=8.0",
        "scikit-image",
        "Wand",
        "opencv-python",
    ],
    extras_require={"dev": ["coverage>=5.5"]},
    license = "MIT",
)