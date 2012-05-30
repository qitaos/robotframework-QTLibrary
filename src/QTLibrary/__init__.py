# -*- coding: cp936 -*-
from keywords import *


from robot.variables import GLOBAL_VARIABLES
from robot import utils
from datetime import date

__version__ = '0.1'

class QTLibrary( _ElementKeywords ):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self):
        """QTLibrary can be imported. By Jacky Qi 
        """
        for base in QTLibrary.__bases__:
            base.__init__(self)









