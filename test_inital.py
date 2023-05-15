from term import Term, NumTerm, VarTerm
from goperator import GOperator
from expression import Expression
import math
import pytest

#Tests for basic operations:

term1 = NumTerm("123")
term2 = NumTerm("634")
assert term1.value == 123
assert term2.value == 634
assert (term1 + term2).value == 757
assert (term1 - term2).value == -511
assert(term1 * term2).value == 77982
assert abs((term1 / term2).value - 0.194006309) < 10 ** -9
assert(term1 ^ term2).value == None
assert(term1 ^ term2).label == "123 ^ 634"