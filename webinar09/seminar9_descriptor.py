class B:
    """
    This is descriptor.

    It can intervene into self's getting, setting and deleting,
    when this instance being reached by attribute access.
    It also has access to "main" object - one that holds this instance as an attribute.

    Details an other examples - https://docs.python.org/3/howto/descriptor.html
    """

    def __init__(self):
        self.value = 1

    def __get__(self, instance, owner=None):
        print('smb gets value')
        print(instance.c)
        return self.value

    def __set__(self, instance, value):
        print('smb sets value')
        if not isinstance(value, int):
            raise ValueError('must be integer')
        self.value = value


class MyClass:
    b = B()

    def __init__(self):
        self.c = 'c'


a = MyClass()
print(a.b)
a.b = '10'  # raising an exception
