DEPRECATED
==========

This project has been deprecated and will no longer be updated.  The original purpose of this project was to make some functionality of the long-defunct distutils2/packaging project available on top of classic distutils/setuptools.  In particular, the ability to provide package configuration declaratively through the ``setup.cfg`` file instead of in ``setup.py``.  This functionality has now been available in plain `setuptools <https://setuptools.readthedocs.io/en/latest/setuptools.html#configuring-setup-using-setup-cfg-files>`_ for some time, and is fairly complete.

Porting
-------

Here is a brief guide for porting ``setup.cfg`` files understood by ``d2to1`` to ``setuptools``, as there are a few slight differences in the section names and syntax.

* Most options supported by the ``[metadata]`` section are the same with a few exceptions.  You can find a complete
  listing of options supported by the ``[metadata]`` section `here <https://setuptools.readthedocs.io/en/latest/setuptools.html#metadata>`_
  
  * ``summary`` -> ``description``: A short description of the package should go in the ``description`` option.
    ``summary`` is still available as an alias for ``description``, however.
  * ``description-file`` -> ``long_description: file:``: A longer description (typically a README) for the package
    goes in the `long_description` option.  This supports a special value in the form ``file: <file1>, <file2>, ...``
    which means the long description is read from a file in the repository given as a relative path.  One or more
    files may be listed (comma-separated).  The `file:` format is available in some other options as well.  See the
    table linked above.
  * ``home-page`` -> ``url``: ``home-page`` is still allowed as an alias but its use is discouraged.
  * ``classifier`` -> ``classifiers``: ``classifier`` is still allowed as an alias but its use is discouraged.
  * ``requires-dist`` -> ``options.install_requires``: This is the same as the ``install_requires`` keyword for the
    ``setup()`` function in ``setuptools``.  It should be moved to the ``[options]`` section of ``setup.cfg``.
    
* The ``[files]`` section no longer exists.  Most options that went under this section now go under a section called 
  ``[options]``.  This includes: ``packages``, ``package_dir``, ``scripts``.  The ``install_requires`` option also goes here,
  among other, more specialized options (including most options from the ``[backwards_compat]`` section of ``d2to1``.

  * The ``options.packages`` option supports a special value ``find:`` which automatically includes any packages
    found (including sub-packages) at the root of the repository (or under the ``package_dir`` directory).  There is
    also a dedicated section ``[options.packages.find]`` which allows passing additional options to control
    how packages are searched, and are equivalent to the keyword arguments accepted by
    `setuptools.find_packages <https://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages>`_.
  * The ``extra_files`` option is not supported; instead, add these files to your project's ``MANIFEST.in``.

* Options that take values consisting of one or more ``<key> = <value>`` pairs have their own sections in the
  new ``setuptools`` format.  These include ``[options.package_data]``, ``[options.data_files]``, ``[options.extras_require]`` and ``[options.entry_points]``.
  
Example
^^^^^^^

Here is an example of ``d2to1``'s ``setup.cfg`` file (the contents of which are listed below in the old README)
ported to the new format::

    [metadata]
    name = d2to1
    version = 0.2.12
    author = Erik M. Bray
    author_email = embray@stsci.edu
    description = Allows using distutils2-like setup.cfg files for a package's metadata with a distribute/setuptools setup.py
    long_description = file: README.rst, CHANGES.rst
    url = http://pypi.python.org/pypi/d2to1
    classifiers = 
        Development Status :: 5 - Production/Stable
        Environment :: Plugins
        Framework :: Setuptools Plugin
        Intended Audience :: Developers
        License :: OSI Approved :: BSD License
        Operating System :: OS Independent
        Programming Language :: Python
        Programming Language :: Python :: 3
        Topic :: Software Development :: Build Tools
        Topic :: Software Development :: Libraries :: Python Modules
        Topic :: System :: Archiving :: Packaging

    [options]
    packages = d2to1, d2to1.extern
    install_requires = setuptools
    # note: the setuptools test command is deprecated since 41.5.0 so this is not useful
    tests_require = nose

    [options.entry_points]
    distutils.setup_keywords = 
        d2to1 = d2to1.core:d2to1
    zest.releaser.prereleaser.middle = 
        d2_version = d2to1.zestreleaser:prereleaser_middle
    zest.releaser.postreleaser.middle = 
        d2_version = d2to1.zestreleaser:postreleaser_middle

Old README follows:

----

Introduction
==============
.. image:: https://travis-ci.org/embray/d2to1.png?branch=master
   :alt: travis build status
   :target: https://travis-ci.org/embray/d2to1

d2to1 (the 'd' is for 'distutils') allows using distutils2-like setup.cfg files
for a package's metadata with a distribute/setuptools setup.py script.  It
works by providing a distutils2-formatted setup.cfg file containing all of a
package's metadata, and a very minimal setup.py which will slurp its arguments
from the setup.cfg.

Note: distutils2 has been merged into the CPython standard library, where it is
now known as 'packaging'.  This project was started before that change was
finalized.  So all references to distutils2 should also be assumed to refer to
packaging.

Rationale
===========
I'm currently in the progress of redoing the packaging of a sizeable number of
projects.  I wanted to use distutils2-like setup.cfg files for all these
projects, as they will hopefully be the future, and I much prefer them overall
to using an executable setup.py.  So forward-support for distutils2 is
appealing both as future-proofing, and simply the aesthetics of using a flat text file to describe a project's metadata.

However, I did not want any of these projects to require distutils2 for
installation yet--it is too unstable, and not widely installed.  So projects
should still be installable using the familiar `./setup.py install`, for
example.  Furthermore, not all use cases required by some of the packages I
support are fully supported by distutils2 yet.  Hopefully they will be
eventually, either through the distutils2 core or through extensions.  But in
the meantime d2to1 will try to keep up with the state of the art and "best
practices" for distutils2 distributions, while adding support in areas that
it's lacking.

Usage
=======
d2to1 requires a distribution to use distribute or setuptools.  Your
distribution must include a distutils2-like setup.cfg file, and a minimal
setup.py script.  For details on writing the setup.cfg, see the `distutils2
documentation`_.  A simple sample can be found in d2to1's own setup.cfg (it
uses its own machinery to install itself)::

    [metadata]
    name = d2to1
    version = 0.2.12
    author = Erik M. Bray
    author-email = embray@stsci.edu
    summary = Allows using distutils2-like setup.cfg files for a package's metadata with a distribute/setuptools setup.py
    description-file =
        README.rst
        CHANGES.rst
    home-page = http://pypi.python.org/pypi/d2to1
    requires-dist = setuptools
    classifier = 
        Development Status :: 5 - Production/Stable
        Environment :: Plugins
        Framework :: Setuptools Plugin
        Intended Audience :: Developers
        License :: OSI Approved :: BSD License
        Operating System :: OS Independent
        Programming Language :: Python
        Programming Language :: Python :: 3
        Topic :: Software Development :: Build Tools
        Topic :: Software Development :: Libraries :: Python Modules
        Topic :: System :: Archiving :: Packaging

    [files]
    packages =
        d2to1
        d2to1.extern
    extra_files =
        CHANGES.rst
        LICENSE
        ez_setup.py

    [backwards_compat]
    zip-safe = False
    tests-require = nose

    [entry_points]
    distutils.setup_keywords = 
        d2to1 = d2to1.core:d2to1
    zest.releaser.prereleaser.middle = 
        d2_version = d2to1.zestreleaser:prereleaser_middle
    zest.releaser.postreleaser.middle = 
        d2_version = d2to1.zestreleaser:postreleaser_middle

The minimal setup.py should look something like this::

 #!/usr/bin/env python

 try:
     from setuptools import setup
 except ImportError:
     from distribute_setup import use_setuptools
     use_setuptools()
     from setuptools import setup

 setup(
     setup_requires=['d2to1'],
     d2to1=True
 )

Note that it's important to specify d2to1=True or else the d2to1 functionality
will not be enabled.  It is also possible to set d2to1='some_file.cfg' to
specify the (relative) path of the setup.cfg file to use.  But in general this
functionality should not be necessary.

It should also work fine if additional arguments are passed to `setup()`,
but it should be noted that they will be clobbered by any options in the
setup.cfg file.

Caveats
=======
- The requires-dist option in setup.cfg is implemented through the
  distribute/setuptools install_requires option, rather than the broken
  "requires" keyword in normal distutils.
- Not all features of distutils2 are supported yet.  If something doesn't seem
  to be working, it's probably not implemented yet.
- Does not support distutils2 resources, and probably won't since it relies
  heavily on the sysconfig module only available in Python 3.2 and up.  This is
  one area in which d2to1 should really be seen as a transitional tool.  I
  don't really want to include a backport like distutils2 does.  In the
  meantime, package_data and data_files may still be used under the [files]
  section of setup.cfg.

.. _distutils2 documentation: http://alexis.notmyidea.org/distutils2/setupcfg.html
