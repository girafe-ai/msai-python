class Point:
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    def __repr__(self):
        return f'({self._x}, {self._y})'

    @staticmethod
    def _validate_float(value: float) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError
        return value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: float):
        self._x = self._validate_float(value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: float):
        self._y = self._validate_float(value)

    def vector_length(self):
        return  # TODO


p = Point(10, 20.5)
print(p.x, p.y)
print(p)

p.x = 5
p.x = 5.5
print(p)
p.x = '123'  # Throw exception
