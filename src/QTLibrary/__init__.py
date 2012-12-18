# -*- coding: cp936 -*-
import os
from keywords import *

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
execfile(os.path.join(THIS_DIR, 'version.py'))

__version__ = VERSION

from robot.variables import GLOBAL_VARIABLES
from robot import utils
from datetime import date

class QTLibrary( _ElementKeywords ):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self):
        """QTLibrary can be imported. By Jacky Qi 
        """
        for base in QTLibrary.__bases__:
            base.__init__(self)









