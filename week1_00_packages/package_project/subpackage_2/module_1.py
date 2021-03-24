# subpackage_2/module_1.py
import os

PATH = os.path.dirname(os.path.abspath(__file__))


def module_func():
    return PATH
