#!/usr/bin/env python
from distutils.core import setup

__version__ = '0.1'

setup(
        name = 'nytCook',
        version = __version__,
        description = 'scrape nytcook',
        platforms=['*nix'],
        requires = ['numpy', 'bs4'],
        provides = ['nytcook'],
        packages = ['nytcook'],
        scripts=['bin/nytcook']
      )
