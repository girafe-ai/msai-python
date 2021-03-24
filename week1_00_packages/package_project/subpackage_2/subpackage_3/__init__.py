# subpackage_3/__init__.py
from .module_1 import module_func as pckg_3_module_func
from .module_2 import module_2_func as pckg_3_module_2_func

__all__ = ['pckg_3_module_func', 'pckg_3_module_2_func']
