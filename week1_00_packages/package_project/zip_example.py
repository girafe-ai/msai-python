# zip_example.py
import sys
from importlib import resources

sys.path.append('zip_package.zip')

import zip_package

print(resources.read_binary(zip_package, "resource.bin"))
# b'binary'