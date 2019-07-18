#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

setup(
    name='currency_cloud',
    version='4.1.0',
    license='MIT',
    description="Python SDK for the Currencycloud API.",
    long_description='',

    author='Francesco Boffa',
    author_email='francesco.boffa@currencycloud.com',
    url='https://connect.currencycloud.com/documentation/getting-started/introduction',

    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    keywords=[],
    install_requires=['requests', 'PyYAML', 'deprecation', 'pytest', 'mock', 'requests-mock', 'betamax', 'betamax-serializers'],
    test_suite='tests'
)
