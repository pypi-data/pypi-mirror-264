from setuptools import setup

__project__ = "pandatorch"
__version__ = "1.0.2"
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

setup(
    name=__project__,
    version=__version__,
    description=__description__,
    packages=__packages__,
    author=__author__,
    author_email=__email__,
    requires=__requires__,
)
