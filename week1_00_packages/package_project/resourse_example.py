# resource_example.py
from importlib import resources
import resource_package

with resources.open_text(resource_package, "resource_file.txt") as res:
    print(res.read())

# Hello, this is resource text file!
# Have a nice day!
