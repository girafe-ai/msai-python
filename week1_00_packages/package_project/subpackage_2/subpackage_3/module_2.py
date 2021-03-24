# subpackage_3/module_2.py
import os

PATH = os.path.dirname(os.path.abspath(__file__))


def module_2_func():
    return PATH
