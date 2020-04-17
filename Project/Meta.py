# Author: Soft9000.com
# 2018/12/31: Class Created

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

class Meta:
    ABOUT           = "Mode: Work-In-Progress!"
    SEPS            = [os.path.sep, "/", "\\"]  # Zero tolerance for path names here.
    UniqueSep       = '.|.'
    ProjType        = ".fgp1"
    DbType          = ".sqlt3"
    DEFAULT_TABLE = "MyTable"
    DEFAULT_FILE_NAME = "./default.sqlt3"
    PRODUCT = "Soft9000/FormGUI."
    VERSION = 0.00
    
    @staticmethod
    def Title():
        return "{0}, Ver. {1} (Alpha)".format(Meta.PRODUCT, Meta.VERSION)
