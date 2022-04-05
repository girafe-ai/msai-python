def uncover_privates(cls):
    """
    Using this decorator you can access "private" name-mangled attributes
    """

    def helper_func(self, name):
        mangled_name = f'_{cls.__name__}{name}'
        if mangled_name in dir(self):
            return getattr(self, mangled_name)
        raise AttributeError

    cls.__getattr__ = helper_func
    return cls


@uncover_privates
class A:
    def __init__(self):
        self.__a = 1
        self.zero = 0

    def __b(self):
        return 2


a = A()

# works thanks to decorator
print(a.__a)
print(a.__b())  # for methods too (methods are just callable attributes)

# also accessible, decorator doesn't break access to existing values
print(a.zero)

# AttributeError exception for non-existing attributes
# print(a.not_existing_attribute)
