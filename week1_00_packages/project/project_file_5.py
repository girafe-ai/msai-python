# project_file_5.py
from sys import (
    getrecursionlimit as get_rec_lim,
    setrecursionlimit as set_rec_lim,
)

get_rec_lim()
set_rec_lim(10000)

print(dir())
# [
# '__annotations__', '__builtins__', '__cached__', '__doc__',
# '__file__', '__loader__', '__name__', '__package__', '__spec__',
# 'get_rec_lim', 'set_rec_lim'
# ]

