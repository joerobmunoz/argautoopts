#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='argautoopts',
    version='0.0.1',
    description='argparse extension to allow automatic declaration of options from class specifications',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Joseph Munoz',
    packages=['argautoopts'],
    install_requires=[],
    license='MIT',
    classifiers=[
            'Programming Language :: Python :: 3'
    ],
    keywords='python dependency injection library',
)