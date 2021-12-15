class A:  # class A(object):
    a = 1

    def __init__(self):
        self.b = 2

    def c(self):
        return 3


class B(A):
    a = 10
    d = 4


class C(B):
    def __init__(self):
        super().__init__()
        self.e = 5


print(issubclass(A, object))  # True
print(issubclass(B, object))  # True
print(issubclass(B, A))       # True

print('*' * 100)

c = C()
print(dir(c))
print(c.a, c.b, c.c(), c.d)  # 10 2 3 4

print('*' * 100)

print(A.a, B.a, C.a)  # 1 10 10
C.a = 20
print(A.a, B.a, C.a)  # 1 10 20

print('*' * 100)


class MachineLearningModel:
    def fit(self, X, y):
        raise NotImplementedError

    def predict(self, X):
        raise NotImplementedError


class LogisticRegression(MachineLearningModel):
    # There you need to implement all abstract methods
    # (unless you want to create new interface)
    pass


class SVM(MachineLearningModel):
    # There you need to implement all abstract methods
    # (unless you want to create new interface)
    pass


print(issubclass(SVM, MachineLearningModel))  # True
print(isinstance(SVM(), MachineLearningModel))    # True
