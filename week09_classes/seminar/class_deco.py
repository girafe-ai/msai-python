def uncover_privates(cls):
    def helper_func(self, name):
        print(name)
    cls.__getattr__ = helper_func
    return cls


@uncover_privates
class A:
    def __init__(self):
        self.__a = 1

    def __b(self):
        return 2


a = A()
print(a.__a)
print(a.__b())
