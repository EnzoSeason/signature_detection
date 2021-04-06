# Signature Detection

A simple tool to detect if there is **a signature** in **an image** or **a PDF file**.

## Installation

1. install [anaconda](https://docs.anaconda.com/anaconda/install/)

2. install packages

    ```
    conda create --name <env> --file requirements.txt
    ```

## Demo

- Image:

    ```
    python demo.py --file my-image.jpeg
    ```

- PDF File:

    ```
    python demo.py --file my-file.pdf
    ```

## Unit Tests

All the codes are covered.

```
cd tests
source coverage.sh
```
 