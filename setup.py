#!/usr/bin/env python

import os
import sys
import warnings

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

base_path = os.path.dirname(__file__)

# Get library version without including the lib
sys.path.insert(0, os.path.join(base_path, 'currencycloud'))
from version import VERSION

# long description
long_description = open(os.path.join(base_path, "README.rst"), "r").read()

setup(
	name='currencycloud',
    version=VERSION,
    description="Python SDK for the Currency Cloud API.",
    long_description=long_description,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='urllib httplib threadsafe filepost http https ssl pooling',
    author='Alessandro Iob',
    author_email='alessandro.iob@toptal.com',
    url='https://connect.currencycloud.com/documentation/getting-started/introduction',
    license='MIT',
    packages=['currencycloud', 'currencycloud.errors', 'currencycloud.actions', 'currencycloud.resources'],
    install_requires=['requests >= 0.8.8', 'PyYAML', 'attrdict'],
    tests_require=[
          'pytest',
          'mock',
          'tox',
          'twine',
          'requests-mock',
          'betamax',
    ],
    test_suite='test',
)
