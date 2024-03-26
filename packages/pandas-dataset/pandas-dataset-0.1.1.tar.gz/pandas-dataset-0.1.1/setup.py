from setuptools import setup, find_packages
from os import path

name = "pandas-dataset"
version = "0.1.1"
description = "Python Datasets on top of Pandas"
url = "https://gitlab.com/meehai/pandas-dataset"

loc = path.abspath(path.dirname(__file__))
with open(f"{loc}/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

required = ["pandas", "numpy", "loguru", "pyarrow"]

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    packages=find_packages(),
    install_requires=required,
    dependency_links=[],
    license="WTFPL",
    python_requires=">=3.8"
)
