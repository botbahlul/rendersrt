#!/usr/bin/env python3
from __future__ import unicode_literals
import os
import sys
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='setuptools')
warnings.filterwarnings("ignore", category=UserWarning, module='setuptools')
warnings.filterwarnings("ignore", message=".*is deprecated*")

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def get_version():
    init_file = os.path.join(os.path.dirname(__file__), 'rendersrt', '__init__.py')
    with open(init_file, 'r') as f:
        for line in f:
            if line.startswith('VERSION'):
                return line.split('=')[1].strip().strip('"\'')

long_description = (
    'rendersrt is a utility for rendering subtitle file into video file'
)

install_requires=[
        "pysrt>=1.0.1",
        "progressbar2>=3.34.3",
]

setup(
    name="rendersrt",
    version=get_version(),
    description="a utility for rendering subtitle file into video file",
    long_description = long_description,
    author="Bot Bahlul",
    author_email="bot.bahlul@gmail.com",
    url="https://github.com/botbahlul/rendersrt",
    packages=["rendersrt"],
    entry_points={
        "console_scripts": [
            "rendersrt = rendersrt:main",
        ],
    },
    install_requires=install_requires,
    license=open("LICENSE").read()
)
