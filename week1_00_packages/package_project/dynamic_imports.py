# dynamic_imports.py
f = __import__(name='functools', globals=globals(), locals=locals())

f = f.partial(lambda x, y: x * y, y=42)
print(f(10))


def _import(name, *args, imp=__import__):
    print(f"Importing module {name!r}")
    return imp(name, *args)

import builtins
builtins.__import__ = _import

from subpackage_2 import *

# Importing module 'subpackage_2'
# Importing module ''
# Importing module 'module_1'
# Importing module 'os'
# Importing module 'module_2'
# Importing module 'os'
# Importing module 'module_1'
# Importing module 'os'
# Importing module 'subpackage_3'

