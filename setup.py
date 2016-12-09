#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-slickqa',
    version='0.1.4',
    author='Chris Saxey',
    author_email='darthghandi@gmail.com',
    maintainer='Chris Saxey',
    maintainer_email='darthghandi@gmail.com',
    license='Apache Software License 2.0',
    url='https://github.com/darthghandi/pytest-slickqa',
    description='A Pytest plugin that reports results to Slickqa',
    long_description=read('README.rst'),
    py_modules=['pytest_slickqa'],
    install_requires=['pytest>=2.9.1', 'slickqa'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],
    entry_points={
        'pytest11': [
            'slickqa = pytest_slickqa',
        ],
    },
)
