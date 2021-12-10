"""
"id" (https://docs.python.org/3/library/functions.html#id):
Return the “identity” of an object.
This is an integer which is guaranteed to be unique and constant for this object during its lifetime.
Two objects with non-overlapping lifetimes may have the same "id()" value.

CPython implementation detail: This is the address of the object in memory.


"is" (https://docs.python.org/3/reference/expressions.html#is-not):
The operators "is" and "is not" test for an object’s identity:
"x is y" is true if and only if "x" and "y" are the same object.
An Object’s identity is determined using the "id()" function.
"x is not y" yields the inverse truth value. [4]

[4] Due to automatic garbage-collection, free lists, and the dynamic nature of descriptors,
you may notice seemingly unusual behaviour in certain uses of the is operator,
like those involving comparisons between instance methods, or constants.
Check their documentation for more info.
"""

import inspect


class Test:
    def test(self):
        pass

    @classmethod
    def test2(cls):
        pass


a = Test()
b = Test()

print('1 (id in memory)   :', id(a.test), '==', id(b.test), '? -', id(a.test) == id(b.test))
print('2 (identity check) :', a.test is b.test)
print('3 (signatures)     :', 'Test.test', inspect.signature(Test.test), ', a.test', inspect.signature(a.test))
print()
print('4 (id in memory)   :', id(a.test2), '==', id(b.test2), '? -', id(a.test2) == id(b.test2))
print('5 (identity check) :', a.test2 is b.test2)
print('6 (signatures)     :', 'Test.test2', inspect.signature(Test.test2), ', a.test2', inspect.signature(a.test2))
