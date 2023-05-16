from term import Term, NumTerm, VarTerm
from goperator import GOperator
from expression import Expression
import math
import pytest

#Tests for basic operations:

plus = GOperator("+")
minus = GOperator("-")
times = GOperator("*")
div = GOperator("/")
pow = GOperator("^")

def getOutTerm(operator, args):
    try: 
        return operator.act(args)
    except: f"Improper arguments in test for {operator}. \nGiven arguments are {args}, but {operator.valence} were required."


def test_numOps():
    term1 = NumTerm("123")
    term2 = NumTerm("634")
    args = [term1, term2]

    assert term1.value == 123
    assert term2.value == 634
    assert getOutTerm(plus, args).value == 757
    assert getOutTerm(minus, args).value == -511
    assert getOutTerm(times, args).value == 77982
    assert abs(getOutTerm(div, args).value - 0.194006309) < 10 ** -9
    assert getOutTerm(pow, args).value == None
    assert getOutTerm(pow, args).label == "123 ^ 634"


def test_varOps():
    term1 = VarTerm("x")
    term2 = VarTerm("y")
    args = [term1, term2]

    assert term1.label == "x"
    assert term2.label == "y"
    assert getOutTerm(plus, args).label == "x + y"
    assert getOutTerm(minus, args).label == "x - y"
    assert getOutTerm(times, args).label == "xy"
    assert getOutTerm(div, args).label == "x / y"
    assert getOutTerm(pow, args).label == "x ^ y"

    term3 = NumTerm("2")
    args = [term1, term3]
    assert term1.label == "x"
    assert term3.label == "2"
    assert getOutTerm(plus, args).label == "x + 2"
    assert getOutTerm(minus, args).label == "x - 2"
    assert getOutTerm(times, args).label == "2x"
    assert getOutTerm(div, args).label == "x / 2"
    assert getOutTerm(pow, args).label == "x ^ 2"

def test_basicExpressions():
    exp1 = Expression("x+y")
    exp2 = Expression("2*x")
    assert str(exp1) == "x + y"
    assert str(exp2) == "2 * x"
    assert str(exp1 + exp2) == "x + y + 2 * x"
    assert str(exp1 - exp2) == "x + y - 2 * x"
    assert str(exp1 * exp2) == "(x + y) * (2 * x)"
    assert str(exp1 / exp2) == "(x + y) / (2 * x)"