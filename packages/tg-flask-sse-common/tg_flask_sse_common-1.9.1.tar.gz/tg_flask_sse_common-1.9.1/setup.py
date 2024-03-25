#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tg_flask_sse_common',
    version='1.9.1',
    author='Tangshimin',
    description='tg_flask_sse_common',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        'tg_flask_sse_common'
    ],
    install_requires=[
        'redis==5.0.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
