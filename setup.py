#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    try:
        from ez_setup import use_setuptools
        use_setuptools()
        from setuptools import setup
    except SyntaxError:
        raise ImportError(
            "d2to1 and projects that use it require setuptools to be "
            "installed; automatic bootstrapping of setuptools is not "
            "supported on Python 2.5")

# d2to1 basically installs itself!  See setup.cfg for the project metadata.
from d2to1.util import cfg_to_args


setup(**cfg_to_args())
