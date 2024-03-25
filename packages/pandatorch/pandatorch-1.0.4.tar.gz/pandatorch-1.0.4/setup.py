from setuptools import setup

__project__ = "pandatorch"
__version__ = "1.0.4"
__description__ = "A flexible simple library that makes it easier to use the extrememly popular pandas package with the other extremely popular framework PyTorch."
__packages__ = ["pandatorch"]
__author__ = "Ashwin U Iyer"
__email__ = "ashwiniyer1706@gmail.com"
__requires__ = [
    "numpy==1.26.4",
    "pandas==1.4.1",
    "pandoc==2.3",
    "pytest==5.4.3",
    "pylint==3.1.0",
    "scikit-learn==1.4.1.post1",
    "torch"
]

setup(
    name=__project__,
    version=__version__,
    description=__description__,
    packages=__packages__,
    author=__author__,
    author_email=__email__,
    install_requires=__requires__,
)
