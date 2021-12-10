from dataclasses import dataclass
from typing import Sequence


@dataclass(eq=False)
class Point:
    x: float
    y: float

    def __post_init__(self):
        self._validate_float(self.x)
        self._validate_float(self.y)

    @staticmethod
    def _validate_float(value: float) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError(f'"{value}" if not float or int')
        return value

    def vector_length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def _validate_compatible(self, other: 'Point' | Sequence) -> 'Point':
        if isinstance(other, self.__class__):
            return other
        elif hasattr(other, '__len__') and len(other) == 2:
            return Point(other[0], other[1])
        else:
            return NotImplemented

    def __eq__(self, other: 'Point' | Sequence):
        other = self._validate_compatible(other)
        if other == NotImplemented:
            return other

        return (self.x, self.y) == (other.x, other.y)

    def __add__(self, other: 'Point' | Sequence):
        other = self._validate_compatible(other)
        if other == NotImplemented:
            return other

        return Point(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return self.__add__(other)


p1 = Point(10, 20.5)
p2 = Point(10, 20.5)
print(p1 == p2)
print(p1 == (10, 20.5))
print((10, 20.5) == p1)
print(p1 + p2)
print(p1 + (1, 2.5))
print(p1 + [1, 2.5])
print((1, 2.5) + p1)
