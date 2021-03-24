# project_file_10.py
from project_file_9 import *

print(dir())
# [
# '__annotations__', '__builtins__', '__cached__',
# '__doc__', '__file__', '__loader__', '__name__',
# '__package__', '__spec__', 'function']

from project_file_9 import _function

print(_function())
# 42

import script_module
# Running demo script for script_module.py: 3