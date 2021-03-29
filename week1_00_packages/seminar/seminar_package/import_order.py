# -*- coding: utf-8 -*-
# dynamic_import_2.py
import builtins
import importlib
import math
import sys
from types import ModuleType
from typing import List, Optional, Union

import scipy


def search_import(
    method: str, modules: List[Union[str, ModuleType]]
) -> Optional[object]:
    for module in modules:
        try:

            if isinstance(module, ModuleType):
                mod = module
            elif isinstance(module, str):
                mod = importlib.import_module(module)
            else:
                raise TypeError('Must be list of strings or ModuleType')

            met = getattr(mod, method, None)

            if met:
                return met

        except ImportError:
            continue

    return None


print(search_import('__import__', ['builtins']))
# <built-in function __import__>

print(search_import('nothing', ['builtins']))
# None


print(search_import('sum', [math, builtins, scipy]))
# <built-in function sum>


print(sys.meta_path)
# [
#   <class '_frozen_importlib.BuiltinImporter'>,
#   <class '_frozen_importlib.FrozenImporter'>,
#   <class '_frozen_importlib_external.PathFinder'>
# ]
