from term import Term, NumTerm, VarTerm
from goperator import GOperator
from expression import Expression
import math

t = GOperator("/")
a = VarTerm(f"x^{math.e}")
b = VarTerm(f"x^{math.pi}")
print(f"{a} {t} {b}")
print(t.act([a, b]))