#!/usr/bin/env python
import codecs
import os
import re
import sys
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def install_requires():

    requires = ['requests', 'aiohttp']
    if sys.version_info > (3, 4):
        requires.extend(['websockets'])
    return requires


setup(
    name='python-kucoin',
    version=find_version("kucoin", "__init__.py"),
    packages=find_packages(exclude=['tests', 'examples']),
    description='Kucoin REST API v3 python implementation',
    url='https://github.com/sammchardy/python-kucoin',
    author='Sam McHardy',
    license='MIT',
    author_email='',
    install_requires=install_requires(),
    keywords='kucoin exchange rest api bitcoin ethereum btc eth kcs',
    classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
