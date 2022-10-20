# -*- coding: utf-8 -*-
from setuptools import setup

__author__ = "Martin Uhrin"
__license__ = "LGPLv3"

about = {}
with open("pytray/version.py") as f:
    exec(f.read(), about)  # nosec

setup(
    name="pytray",
    version=about["__version__"],
    description="A python tools library for baking pies",
    long_description=open("README.rst").read(),
    url="https://github.com/muhrin/pytray.git",
    author="Martin Uhrin",
    author_email="martin.uhrin.10@ucl.ac.uk",
    license=__license__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="tools utilities",
    install_requires=["deprecation"],
    python_requires=">=3.7",
    extras_require={
        "dev": [
            "grayskull",
            "pip",
            "pre-commit",
            "pytest",
            "pytest-cov",
            "ipython<6",
            "twine",
        ],
        "docs": [
            "Sphinx==1.8.4",
            "Pygments==2.3.1",
            "docutils==0.14",
        ],
    },
    packages=["pytray"],
    test_suite="test",
)
