# Update PyPi

## Update `setup.py`

`version` need to be update.

## Build

```bash
python setup.py bdist_wheel sdist
```

## Upload

```bash
twine upload dist/*
```