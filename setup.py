#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    import sys
    if sys.version_info[:2] < (2, 6):
        from ez_setup25 import use_setuptools
    else:
        from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

# d2to1 basically installs itself!  See setup.cfg for the project metadata.
from d2to1.util import cfg_to_args


setup(**cfg_to_args())
