# subpackage_2/__init__.py
from . import subpackage_3
from .module_1 import module_func as pckg_2_module_func
from .subpackage_3 import *

__all__ = ['pckg_2_module_func'] + subpackage_3.__all__
