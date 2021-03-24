# project_file_9.py
__all__ = ['function']


INTERNAL_CONSTANT = 42


def _function():
    return INTERNAL_CONSTANT


def function():
    return _function()




