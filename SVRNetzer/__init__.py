"""
SVRNetzer is a Python library used in the STRING Extension for the VRNetzer.

See the webpage for more information and documentation:

    

"""
import sys

if sys.version_info < (3, 9):
    raise ImportError("Python version 3.9 or above is required for SymPy.")
del sys

from .util import converter, settings, util
