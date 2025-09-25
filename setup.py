#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

setup(
    name='currency_cloud',
    version='7.1.0',
    license='MIT',
    description="Python SDK for the Currencycloud API.",
    long_description='',

    author='Currencycloud',
    author_email='sdk@currencycloud.com',
    url='https://github.com/CurrencyCloud/currencycloud-python',

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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    keywords=[],
    install_requires=['requests', 'PyYAML', 'deprecation'],
    tests_require=[
        'pytest', 'mock', 'requests-mock', 'betamax', 'betamax-serializers'
    ],
    test_suite='tests'
)
