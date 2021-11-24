@classmethod
def foo(*args, **kwargs):
    print(args, kwargs)


class Test:
    d = {}

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


a = Test()
a.bar()

print(Test)
print(a.b)
print(a.b)

# a._Test__b = 3
# print(a._Test__b)

# a = Test()
# Test.d['1'] = '1'
# b = Test()
#
# a.test_3()
# Test.test_3()

# print(type(a))
# print(type(Test))
