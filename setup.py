#!/usr/bin/env python
from setuptools import setup

setup(
    name='python-kucoin',
    version='2.0.0',
    packages=['kucoin'],
    description='Kucoin REST API v2 python implementation',
    url='https://github.com/sammchardy/python-kucoin',
    author='Sam McHardy',
    license='MIT',
    author_email='',
    install_requires=['requests'],
    keywords='kucoin exchange rest api bitcoin ethereum btc eth kcs',
    classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
