from functools import reduce

"""
A small expressions language
"""

# https://docs.python.org/3/library/operator.html
# typically neg looks like
# neg = lambda x: -x
# and add is like
# add = lambda x, y: x + y

from operator import neg, add, sub, mul, truediv


class Atom:
    """
    a class to implement an atomic value,
    like an int, a float, a str, ...

    in order to be able to use this,
    child classes need to provide self.type
    that should be a class like int or float
    or similar whose constructor expects one arg
    """
    def __init__(self, value):
        self.value = self.type(value)

    def eval(self):
        return self.value



class Unary:
    """
    the mother of all unary operators

    in order to be able to use this,
    child classes need to provide self.function
    which is expected to be a 1-parameter function
    """
    def __init__(self, operand):
        self.operand = operand

    def eval(self):
        """
        """
        try:
            return self.function(self.operand.eval())
        except AttributeError:
            print(f"WARNING - class {self.__class__.__name__} lacks a function")


class Binary:
    """
    the mother of all binary operators

    in order to be able to use this,
    child classes need to provide self.function
    which is expected to be a 2-parameter function
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        try:
            return self.function(self.left.eval(),
                                 self.right.eval())
        except AttributeError:
            print(f"WARNING - class {self.__class__.__name__} lacks a function")


class Nary:
    """
    the mother of all n-ary operators

    self.function is expected to be a 2-ary associative function
    and evaluation is performed through a call to reduce()
    """
    # 2 parameters are required
    def __init__(self, left, right, *more):
        self.children = [left, right, *more]

    def eval(self):
        try:
            return reduce(self.function, (x.eval() for x in self.children))
        except AttributeError:
            print(f"WARNING - class {self.__class__.__name__} lacks a function")


######
class Integer(Atom):
    type = int
class Float(Atom):
    type = float


class Negative(Unary):
    function = neg


class Minus(Binary):
    function = sub
class Divide(Binary):
    function = truediv


class Plus(Nary):
    function = add
class Multiply(Nary):
    function = mul
