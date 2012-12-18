#!/usr/bin/env python

#  Copyright (c) 2010 Franz Allan Valencia See
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


"""Setup script for Robot's QTLibrary distributions"""


try:
    from ez_setup import use_setuptools
    use_setuptools()
except ImportError:
    pass

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from os.path import join, dirname
execfile(join(dirname(__file__), 'src', 'QTLibrary', 'version.py'))

DESCRIPTION = """
QTLibrary is a web testing library for Robot Framework
that leverages the Selenium 2 (WebDriver) libraries.
"""[1:-1]

setup(name         = 'robotframework-qtlibrary',
      version      = VERSION,
      description  = 'QTLibrary for Robot Framework',
      long_description = DESCRIPTION,
      author       = 'Qitao',
      author_email = 'Qitao016@pingan.com',
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
      packages     = ['QTLibrary','QTLibrary.keywords']
      )

