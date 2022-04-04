from abc import ABC, abstractmethod


class AbstractPoint(ABC):
    @abstractmethod
    def __add__(self, other_point: 'AbstractPoint'):
        ...

    @abstractmethod
    def __repr__(self):
        ...

    @property
    @abstractmethod
    def vector_length(self) -> float:
        ...


class Test(AbstractPoint):
    def __add__(self, other_point: 'Point2D'):
        pass  # TODO


# test = Test()


class Point2D(AbstractPoint):

    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    def __add__(self, other_point: 'Point2D'):
        pass  # TODO

    def __repr__(self):
        return "".join(["Point(", str(self._x), ",", str(self._y), ")"])

    @property
    def vector_length(self) -> float:
        return (self._x ** 2 + self._y ** 2) ** 0.5


print(Point2D(2, 1).vector_length)


class Point3D(AbstractPoint): pass
class PointMD(AbstractPoint): pass