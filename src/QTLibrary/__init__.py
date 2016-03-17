#encoding=utf-8
import os
from keywords import *

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
execfile(os.path.join(THIS_DIR, 'version.py'))

__version__ = VERSION

from robot import utils
from datetime import date

class QTLibrary(
    _ElementKeywords,
    _LoggingKeywords,
    _RunOnFailureKeywords,
):
    """QTLibrary是一个个人学习研究时做的测试库，参考了一下Selenium2Library的一些写法.
    其中做了几个比较常用的关键字，比如随机生成生日，随机生成身份证号，随机生成中文姓名等。
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self):
        """QTLibrary can be imported. By Jacky Qi 
        """
        for base in QTLibrary.__bases__:
            base.__init__(self)









