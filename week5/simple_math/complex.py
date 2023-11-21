class Complex:
    def __init__(self, real: float, img: float):
        self.real = real
        self.img = img
    
    def __repr__(self) -> str:
        return f"{self.real} + {self.img}i"

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(self.real + other, self.img)
        elif isinstance(other, self.__class__):
            return self.__class__(self.real + other.real, self.img + other.img)
        else:
            raise ValueError(f"Cannot add {self.__class__} and {other.__class__}")

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(self.real - other, self.img)
        elif isinstance(other, self.__class__):
            return self.__class__(self.real - other.real, self.img - other.img)
        else:
            raise ValueError(f"Cannot subtract {self.__class__} and {other.__class__}")
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            other = self.__class__(other, 0)
        if isinstance(other, self.__class__):
            return self.__class__(
                self.real * other.real - self.img * other.img,
                self.real * other.img + self.img * other.real
            )
        else:
            raise ValueError(f"Cannot multiply {self.__class__} and {other.__class__}")
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(other - self.real, -self.img)
    
    __rmul__ = __mul__

    def __eq__(self, other):
        if isinstance(other, (int, float)):
            return self.real == other and self.img == 0
        elif isinstance(other, self.__class__):
            return self.real == other.real and self.img == other.img
        else:
            raise ValueError(f"Cannot compare {self.__class__} and {other.__class__}")
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __neg__(self):
        return self.__class__(-self.real, -self.img)

    def __lt__(self, other):
        if isinstance(other, (int, float)):
            return self.real < other
        elif isinstance(other, self.__class__):
            return self.real < other.real
        else:
            raise ValueError(f"Cannot compare {self.__class__} and {other.__class__}")
    
    def __gt__(self, other):
        if isinstance(other, (int, float)):
            return self.real > other
        elif isinstance(other, self.__class__):
            return self.real > other.real
        else:
            raise ValueError(f"Cannot compare {self.__class__} and {other.__class__}")
    
    def __bool__(self):
        return self.real != 0 or self.img != 0