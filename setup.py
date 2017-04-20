#!/usr/bin/env python

from os.path import abspath, dirname, join

from setuptools import setup

CURDIR = dirname(abspath(__file__))
version_file = join(CURDIR, 'src', 'QTLibrary', 'version.py')
try:
    execfile(version_file)
except NameError:
    exec(compile(open(version_file).read(), version_file, 'exec'))

DESCRIPTION = """
QTLibrary is a web testing library for Robot Framework
that leverages the QTLibrary libraries.
"""[1:-1]

with open(join(CURDIR, 'requirements.txt')) as f:
    REQUIREMENTS = f.read().splitlines()
    
setup(name         = 'robotframework-qtlibrary',
      version      = VERSION,
      description  = 'QTLibrary for Robot Framework',
      long_description = DESCRIPTION,
      author       = 'Qitao',
      author_email = 'Qitaos@gmail.com',
      url          = 'https://github.com/qitaos/Robotframework-QTLibrary',
      license      = 'Apache License 2.0',
      keywords     = 'robotframework qtlibrary',
      platforms    = 'any',
      classifiers  = [
                        "Development Status :: 5 - Production/Stable",
                        "License :: OSI Approved :: Apache Software License",
                        "Operating System :: OS Independent",
                        "Programming Language :: Python",
                        "Topic :: Software Development :: Testing"
                     ],
      install_requires = REQUIREMENTS,
      package_dir  = {'' : 'src'},
      packages     = ['QTLibrary','QTLibrary.keywords'],
      include_package_data = True,
      )

