from .complex import Complex


class Point(Complex):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
    
    def __repr__(self) -> str:
        return f"({self.real}, {self.img})"
    
    def distance(self, other: "Point") -> float:
        return ((self.real - other.real)**2 + (self.img - other.img)**2)**0.5

    def length(self) -> float:
        return self.distance(self.__class__(0, 0))