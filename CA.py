# Gracious Computer-Algebra
# Author: Grace Unger
# Stores an input string as a list of tokens
# and handles basic operations to manipulate

import math
class Symbol:
    operators = {"*":3, "-":2, "+":2, "/":3, "^":4,
                 "sin":5, "cos":5, "tan":5, "log":5}
    reserved=("*", "-", "+", "/", "sin", "cos", "tan", "(", ")")
    opRules={"*": lambda x,y: x*y, "+": lambda x,y: x+y,
             "-": lambda x,y:x-y, "/": lambda x,y: x/y,
             "sin": lambda x: math.sin(x), "cos": lambda x:math.cos(x),
             "tan": lambda x :math.tan(x), "log": lambda x:math.log(x)}

    def __init__(self, name):
        self.tokenized = []
        for i in name:
            self.tokenized.append(i)

    def __str__(self):
        return ''.join(x for x in self.tokenized)

    def __add__(self, addend):
        return Symbol(f"{self}+{addend}")

    def __sub__(self, subtrahend):
        return Symbol(f"{self}-{subtrahend}")

    def __mul__(self, factor):
        return Symbol(f"{self}*{factor}")

    @staticmethod
    def par(exp):
        return Symbol(f"({exp})")

    @staticmethod
    def eval(exp):
        out = []
        op = []
        for i in exp:
            if not i in Symbol.reserved: out += i+" "
            if i in op:
                while Symbol.operators[op[-1]]>Symbol.operators[i]:
                    out.append(op.pop())
                op.append(i)
            if i == "(": op.append("(")
            if i == ")":
                while not op[-1]=="(":out.append(op.pop())
                out.append(op.pop())
        while op:out.append(op.pop())
        value = []
        temp = []
        while out:
            temp.append(out[0])
            out = out[1:]
            if temp[-1] in operator



