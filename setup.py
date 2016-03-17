#!/usr/bin/env python

import sys
from os.path import join, dirname
sys.path.append(join(dirname(__file__), 'src'))
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup
execfile(join(dirname(__file__), 'src', 'QTLibrary', 'version.py'))

DESCRIPTION = """
QTLibrary is a web testing library for Robot Framework
that leverages the QTLibrary libraries.
"""[1:-1]

setup(name         = 'robotframework-qtlibrary',
      version      = VERSION,
      description  = 'QTLibrary for Robot Framework',
      long_description = DESCRIPTION,
      author       = 'Qitao',
      author_email = 'Qitaos@gmail.com',
      url          = 'https://github.com/qitaos/Robotframework-QTLibrary',
      license      = 'No License',
      platforms    = 'any',
      classifiers  = [
                        "Development Status :: 5 - Production/Stable",
                        "License :: OSI Approved :: Apache Software License",
                        "Operating System :: OS Independent",
                        "Programming Language :: Python",
                        "Topic :: Software Development :: Testing"
                     ],
      install_requires = [
							
						 ],
      py_modules=['ez_setup'],
      package_dir  = {'' : 'src'},
      packages     = ['QTLibrary','QTLibrary.keywords'],
      include_package_data = True,
      )

