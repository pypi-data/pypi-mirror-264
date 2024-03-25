from setuptools import setup

__project__ = "pandatorch"
__version__ = "1.0.3"
__description__ = "A flexible simple library that makes it easier to use the extrememly popular pandas package with the other extremely popular framework PyTorch."
__packages__ = ["pandatorch"]
__author__ = "Ashwin U Iyer"
__email__ = "ashwiniyer1706@gmail.com"
__requires__ = [
    "numpy",
    "pandas",
    "pandoc",
    "pytest",
    "pylint",
    "sklearn",
]
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name=__project__,
    version=__version__,
    description=__description__,
    packages=__packages__,
    author=__author__,
    author_email=__email__,
    requires=__requires__,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
