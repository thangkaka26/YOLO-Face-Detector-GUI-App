import sys
sys.dont_write_bytecode = True

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from ui.gui import GUI

GUI()