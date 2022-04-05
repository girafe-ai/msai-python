def foo(*args, **kwargs):
    print(args, kwargs)


class Test:
    d = {}

    # Class variable is method if it is callable.
    # By default, first argument of method is self, even if function created outside the class.
    bar = foo

    def __init__(self):
        self.a = 1
        self.__b = 2  # name mangling
        self.c = {}

    def __repr__(self):
        return f'Test({self.a}, {self.__b}, {self.c}, {self.d})'

    def test_2(self):
        print(self.a)

    @classmethod
    def test_3(cls):
        print(cls.d)

    @property
    def b(self):
        print('b was touched')
        return self.__b


# running a method
a = Test()
a.bar()

# accessing property
print(Test)
print(a.b)

# accessing "private" attribute
print(a._Test__b)
a._Test__b = 3
print(a._Test__b)

# class attributes are common for all instances of class
# because they are attached to a class, not to specific instance
a = Test()
Test.d['1'] = '1'
b = Test()
print(a.d, Test.d, b.d)

# classmethod-decorated methods are also attached to a class
a.test_3()
Test.test_3()

# classes are objects, so they have types too
print(type(a))
print(type(Test))
