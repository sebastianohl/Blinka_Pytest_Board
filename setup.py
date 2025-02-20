#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2025 Sebastian Ohl
#
# SPDX-License-Identifier: MIT

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

setup(
    name="Blinka-Pytest-Board",
    description="Python Test Blinka Board Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sebastian Ohl",
    author_email="sebastian@ohl.name",
    python_requires=">=3.7.0",
    url="https://github.com/sebastianohl/Blinka_Pytest_Board.git",
    #package_dir={"": "pytest_board_client"},
    packages=["pytest_board_client"],
    install_requires=[
        "Adafruit_Blinka", "Adafruit-Blinka-Displayio",
        "Adafruit-Blinka-Displayio", "adafruit-circuitpython-display-text",
        "adafruit-circuitpython-st7789", "adafruit-circuitpython-neopixel"
    ],
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: MicroPython",
    ],
)
