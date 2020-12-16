from functools import reduce

"""
A small expressions language, with variables and assignment

as a result we have 3 additions to the AST nodes menagerie
* Expressions to build a program block
* Assignment to store a result in a variable name
* Variable to reference a variable (use latest stored value)
"""

# https://docs.python.org/3/library/operator.html
# typically neg looks like
# neg = lambda x: -x
# and add is like
# add = lambda x, y: x + y

from operator import neg, add, sub, mul, truediv


class Expression:
    """
    for compatibility with v1
    we need our expressions to be able to do eval()
    with possibly no argument

    so our child classes will implement _eval(env) (mandatory arg)
    and this layer deals with creating an empty env when needed
    """
    def eval(self, env=None):
        if env is None:
            env = {}
        return self._eval(env)

    def _eval(self, env):
        print(f"{type(self).__name__} needs to implement _eval(env)")


class Atom(Expression):
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

    def _eval(self, env):
        return self.value



class Unary(Expression):
    """
    the mother of all unary operators

    in order to be able to use this,
    child classes need to provide self.function
    which is expected to be a 1-parameter function
    """
    def __init__(self, operand):
        self.operand = operand

    def _eval(self, env):
        """
        """
        try:
            return self.function(self.operand.eval(env))
        except AttributeError:
            print(f"WARNING - class {self.__class__.__name__} lacks a function")


class Binary(Expression):
    """
    the mother of all binary operators

    in order to be able to use this,
    child classes need to provide self.function
    which is expected to be a 2-parameter function
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def _eval(self, env):
        try:
            return self.function(self.left.eval(env),
                                 self.right.eval(env))
        except AttributeError:
            print(f"WARNING - class {self.__class__.__name__} lacks a function")


class Nary(Expression):
    """
    the mother of all n-ary operators

    self.function is expected to be a 2-ary associative function
    and evaluation is performed through a call to reduce()
    """
    # 2 parameters are required
    def __init__(self, left, right, *more):
        self.children = [left, right, *more]

    def _eval(self, env):
        try:
            return reduce(self.function, (x.eval(env) for x in self.children))
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



class Expressions(Expression):
    """
    a sequence of expressions
    its result is the result of the last expression
    """
    def __init__(self, mandatory, *optional):
        # optional is bound to a tuple
        self.children = [mandatory] + list(optional)

    def _eval(self, env):
        last_result = None
        for child in self.children:
            last_result = child.eval(env)
        return last_result


class Assignment(Expression):
    """
    Assignment(varname, expression) evaluates the expression,
    assigns the result to varname, and returns that result
    """
    def __init__(self, varname, expression):
        self.varname = varname
        self.expression = expression

    def _eval(self, env):
        result = self.expression.eval(env)
        env[self.varname] = result
        return result


class Variable(Expression):
    """
    returns the value of that variable
    """
    def __init__(self, varname):
        self.varname = varname

    def _eval(self, env):
        # keep it simple for now
        # our language does not support exceptions, so
        # let us return None on undefined variables
        return env.get(self.varname, None)

