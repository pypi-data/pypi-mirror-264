import setuptools
from pathlib import Path

setuptools.setup(
    name="UPLOADS_PYPI",
    version=1.0,
    long_description=Path("Readme.md").read_text(),
    packages=setuptools.find_packages(exclude=["_amstrong_number.py"])
)