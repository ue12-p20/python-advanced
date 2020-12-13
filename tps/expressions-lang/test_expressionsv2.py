# because we have not yet learned about unittest
# we implement a super lightweight micro test framework
#
# all functions whose name starts with test_
# are considered test cases

# the code to test
from expressions2 import (
    Integer, Float, Negative, Plus, Minus, Multiply, Divide,
    Expressions, Assignment, Variable
    )


# the test cases
def test_001():
    ####
    # in some earlier pass, the source code text has been parsed
    # and as a result we build an AST
    #
    # for example, this code
    # exp = (10 * 2 + 30) * (-4 * 25)
    # would result in this AST
    tree = Multiply(
        Plus(Multiply(Integer(10), Integer(2)), Integer(30)),
        Multiply(Negative(Integer(4)), Integer(25)))

    assert tree.eval() == -5000

def test_002():
    tree = Plus(Multiply(Integer(10), Integer(2)),
                Negative(Negative(Integer(30))),
                Minus(Integer(100), Integer(50)))

    assert tree.eval() == 100

def test_003():
    tree = Multiply(
        Plus(Integer(30), Integer(40), Integer(50)),
            Minus(Integer(20), Integer(15)))

    assert tree.eval() == 600

def test_004():
    tree = Negative(
        Plus(Float(10), Negative(Integer(20))))

    assert tree.eval() == 10.

def test_005():
    tree = Divide(Integer(10), Integer(4))
    assert tree.eval() == 2.5

def test_006():
    ########
    try:
        Multiply()
    except TypeError:
        print("OK")

def test_007():
    try:
        Plus(Integer(1))
    except TypeError:
        print("OK")

def test_008():
    try:
        Negative(Integer(10), Integer(20))
    except TypeError:
        print("OK")

def test_009():
    try:
        Divide(Integer(10), Integer(20), Integer(30))
    except TypeError:
        print("OK")


def test_100():
    """
    a = 10
    b = 20
    a + b
    """
    program = Expressions(
        Assignment("a", Integer(10)),
        Assignment("b", Integer(20)),
        Plus(Variable("a"), Variable("b")),
    )

    assert program.eval() == 30


def test_101():
    """
    a = 2 + (b := 2) # env = {'a': 4, 'b': 2}
    b = a * b        # env = {'a': 4, 'b': 8}
    b * b            # env - unchanged
    """
    program = Expressions(
        Assignment("a", Plus(Integer(2),
                             Assignment("b", Integer(2)))),
        Assignment("b", Multiply(Variable("a"), Variable("b"))),
        Multiply(Variable("b"), Variable("b")),
    )

    assert program.eval() == 64



# the micro test engine
# of course, that would need
# * the ability to select test cases
# * nicer reporting
# * statistics
# * and so on
# which is what a decent test framework
# like pytest brings for free

import types
def run_all_tests():
    for symbol in globals():
        if symbol.startswith('test_') and isinstance(symbol, types.FunctionType):
            symbol()


# run the engine if this module is passed directly to python
if __name__ == '__main__':
    run_all_tests()
