# Python Runtime (Expiration Checker)

![PyPI](https://img.shields.io/pypi/v/python_runtime)

`python_runtime` is a Python package providing middleware for FastAPI applications that restricts access to the service past a specified expiration date. The expiration date is dynamically determined based on the package version, following the format `YY.M.DD`, where `YY` is the year, `M` is the month, and `DD` is the day.

## Installation

To install `python_runtime`, run the following command in your terminal:

```bash
pip install python_runtime==version_number
```

## Intall locally

To install `python_runtime` locally, run the following command in your terminal:

```bash
pip install -e .
```

## Instructions to publish package

1. Update the version number in `setup.py` and `README.md`.
2. Run the following command in your terminal:

```bash
python setup.py sdist bdist_wheel
```

3. Run the following command in your terminal:

```bash
twine upload dist/*
```
