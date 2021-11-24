class StrList:
    """
    StrList is list-like container for strings.
    """

    PRINT_COUNT = 3

    def __init__(self, state: list[str] | None = None, max_length: int | None = None):
        self._state = self._validate_state(state)
        self._max_length = self._validate_int(max_length) if max_length is not None else None
        self._trim_state()

    @classmethod
    def _validate_state(cls, state: list[str] | None) -> list[str]:
        if state is None:
            return []

        if not isinstance(state, list):
            raise TypeError(f'state of {cls.__name__} must be list[str]')

        for element in state:
            if not isinstance(element, str):
                raise TypeError(f'state of {cls.__name__} must be list[str]')

        return state

    @staticmethod
    def _validate_str(element: str) -> str:
        if not isinstance(element, str):
            raise TypeError('element must be str')
        return element

    @staticmethod
    def _validate_int(value: int) -> int:
        if not isinstance(value, int):
            raise TypeError('value must be int')
        if value <= 0:
            raise ValueError('value must be positive integer')
        return value

    def _trim_state(self):
        if self._max_length is not None:
            self._state = self._state[:self._max_length]

    def get_state(self) -> list[str]:
        return self._state.copy()

    @property
    def max_length(self) -> int | None:
        return self._max_length

    @max_length.setter
    def max_length(self, max_length: int):
        self._max_length = self._validate_int(max_length)
        self._trim_state()

    @max_length.deleter
    def max_length(self):
        self._max_length = None

    def append(self, element: str) -> None:
        self._state.append(self._validate_str(element))
        self._trim_state()

    def extend(self, state: list[str] | None = None) -> None:
        self._state += self._validate_state(state)
        self._trim_state()

    def remove(self, element: str) -> None:
        self._state.remove(element)

    def print(self):
        elements_to_print = self._state[:self.PRINT_COUNT]
        print(f'StrList({len(self._state)}): {elements_to_print}')


print(StrList()._state)  # []
print(StrList()._state)  # []
print(StrList(['1'])._state)  # ['1']
print(StrList(['abc', 'def', 'ghi'])._state)  # ['abc', 'def', 'ghi']

# StrList(1)  # TypeError
# StrList([1, 2, 3])  # TypeError
# StrList({'1'})  # TypeError


sl = StrList(['a', 'b'])
sl.append('c')
sl.extend(['d', 'e'])
sl.remove('c')
print(sl.get_state())  # ['a', 'b', 'd', 'e']


sl = StrList(['a', 'b', 'c', 'd', 'e'])
sl.print()  # "StrList(5): ['a', 'b', 'c']"


print(StrList.__dict__)
# {'__module__': '__main__',
#  '__doc__': '\n    StrList is list-like container for strings.\n    ',
#  'PRINT_COUNT': 3,
#  '__init__': <function StrList.__init__ at 0x10d912710>,
#  '_validate_state': <classmethod(<function StrList._validate_state at 0x10d912680>)>,
#  '_validate_str': <staticmethod(<function StrList._validate_str at 0x10d9127a0>)>,
#  '_validate_int': <staticmethod(<function StrList._validate_int at 0x10d912830>)>,
#  '_trim_state': <function StrList._trim_state at 0x10d9128c0>,
#  'get_state': <function StrList.get_state at 0x10d912950>,
#  'max_length': <property object at 0x10d90b420>,
#  'append': <function StrList.append at 0x10d912b90>,
#  'extend': <function StrList.extend at 0x10d912c20>,
#  'remove': <function StrList.remove at 0x10d912cb0>,
#  'print': <function StrList.print at 0x10d912d40>,
#  '__dict__': <attribute '__dict__' of 'StrList' objects>,
#  '__weakref__': <attribute '__weakref__' of 'StrList' objects>}

print(StrList(['a', 'b', 'c']).__dict__)
# {'_state': ['a', 'b', 'c'], '_max_length': None}

print(dir(StrList()))
# ['PRINT_COUNT', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
#  '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__',
#  '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__',
#  '__subclasshook__', '__weakref__', '_max_length', '_state', '_trim_state', '_validate_int', '_validate_state',
#  '_validate_str', 'append', 'extend', 'get_state', 'max_length', 'print', 'remove']


sl = StrList(max_length=10)
print(sl.max_length)  # 10
sl.max_length = 50
print(sl.max_length)  # 50
del sl.max_length
print(sl.max_length)  # None
