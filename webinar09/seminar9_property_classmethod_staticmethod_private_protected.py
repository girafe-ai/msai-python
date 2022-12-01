class MyClass:
    def __init__(self):
        self._b = 1  # protected variable - can be used from outside, but it is not recommended
        self.__b = 1  # hidden (private) variable - can't be used from outside by its name

    @property
    def b(self):
        """
        Property works like attribute,
        but intercept getting, setting (optionally) and deleting (optionally).

        Basically property allows to create descriptor right in class.
        """
        return self.__b

    @b.setter
    def b(self, new_value):
        print('smb changing value')
        self.__b = new_value

    @staticmethod
    def helper_power(a, b):
        """
        `staticmethod` doesn't require instance.
        It can be called from class and from instance.
        """
        return a * b

    @classmethod
    def helper_create(cls):
        """
        `classmethod` doesn't require instance but depends on class.
        Like `staticmethod` it can be called from class and from instance.

        `cls` contains current class.
        It is recommended to use `cls`, not `MyClass` hardcoded -
         in inherited classes classmethods will use their class, not `MyClass`.
        """
        return cls()


a = MyClass()
print(a.b)  # calling property getter
a.b = '10'  # calling property setter


print(MyClass.helper_power(5, 6))
print(MyClass.helper_create())
print(MyClass().helper_power(5, 6))
print(MyClass().helper_create())


class MyClass2(MyClass):
    def c(self):
        print(self.__b)  # can access hidden (private) var on inheritance


print('1:', MyClass2.helper_power(5, 6))

# it will create MyClass2 instance (not MyClass)
# because helper_create uses `cls` which is MyClass2
print('3:', MyClass2.helper_create())
