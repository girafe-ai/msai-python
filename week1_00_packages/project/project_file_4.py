# project_file_4.py
import math as m

print(m)
# <module 'math' from '/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/lib-dynload/math.cpython-37m-darwin.so'>

print(type(m))
# <class 'module'>

print(dir())
# ['__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'm']


# Almost the same as
import math

m = math

print(dir())
# ['__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'm', 'math']
