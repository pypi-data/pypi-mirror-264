import setuptools
from pathlib import Path

setuptools.setup(
    name="madavOddEven",
    version=1.0,
    long_description=Path("Readme.md").read_text(),
    packages=setuptools.find_packages(exclude=["odd_eve"])
)