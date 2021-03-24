# project_file_3.py
import project_file_2

# Simple project file func
# 10

print(dir(project_file_2))
# ['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'project_file_1']

from project_file_2 import project_file_1
print(dir(project_file_1))
# ['SIMPLE_CONSTANT', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'itertools', 'project_file_func']
print(type(project_file_1))
# <class 'module'>

