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
term1 = NumTerm("123")
term2 = NumTerm("634")
args = [term1, term2]

def test_numOps():

    assert term1.value == 123
    assert term2.value == 634
    assert getOutTerm(plus, args).value == 757
    assert getOutTerm(minus, args).value == -511
    assert getOutTerm(times, args).value == 77982
    assert abs(getOutTerm(div, args).value - 0.194006309) < 10 ** -9
    assert getOutTerm(pow, args).value == None
    assert getOutTerm(pow, args).label == "123 ^ 634"
