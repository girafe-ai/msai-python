from typing import Sequence


class Point2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

    def _validate_compatible(self, other: 'Point2D' | Sequence) -> 'Point2D':
        if isinstance(other, self.__class__):
            return other
        elif hasattr(other, '__len__') and len(other) == 2:
            return Point2D(other[0], other[1])
        else:
            return NotImplemented

    def __add__(self, other_point: 'Point2D'):
        other = self._validate_compatible(other_point)
        if other == NotImplemented:
            return other

        return Point2D(self.x + other.x, self.y + other.y)


class StringPointAdapter(Point2D):
    def __init__(self, s: str):
        s = s.replace('(', '').replace(')', '').replace(' ', '')
        try:
            x_str, y_str = s.split(',')
            x, y = float(x_str), float(y_str)
        except ValueError:
            raise ValueError('StringPointAdapter format is (2.0, 4.0)')

        super().__init__(x, y)


print(Point2D(1, 5) + Point2D(2, 4))
print(Point2D(1, 5) + StringPointAdapter('(2, 4)'))
