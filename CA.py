# Gracious Computer-Algebra
# Author: Grace Unger
# Created: 1-8-23
# Modified: 1-8-23
# Stores an input string as a list of tokens
# and evaluates simple expressions according to a Shunting Yard algorithm
#
#

import math
class Symbol:
    operators = {"*":3, "-":2, "+":2, "/":3, "^":4,
                 "sin":5, "cos":5, "tan":5, "log":5}
    reserved=("*", "-", "+", "/", "sin", "cos", "tan", "(", ")")
    opRules={"*": lambda x,y: x*y, "+": lambda x,y: x+y,
             "-": lambda x,y:x-y, "/": lambda x,y: x/y,
             "sin": lambda x: math.sin(x), "cos": lambda x:math.cos(x),
             "tan": lambda x :math.tan(x), "log": lambda x:math.log(x)}
    opArgs = {"*":2, "-":2, "+":2, "/":2, "^":2,
                 "sin":1, "cos":1, "tan":1, "log":1}

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
    # Symbol -> Symbol
    # Uses Shunting Yard algorithm to convert input to RPN output, reads output to evaluate.
    # Numerical values are properly evaluated and symbolic values are converted back, into symbols
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
        temp = []
        while out:
            temp.append(out[0])
            out = out[1:]
            if temp[-1] in operators:
                opr = temp[-1]
                if opArgs[opr] == 1:
                    if temp[-2]:
                        if isdigit(temp[-2]): out = [opRules[opr](temp[-2]) + ''] + out
                        else: out = [Symbol(f"{opr}({temp[-2]})")]
                    else:
                        print(f"Operator {opr} has insufficient arguments")
                        return
                if opArgs[opr] == 2:
                    if not temp[-2] or not temp[-3]:
                        print(f"Operator {opr} has insufficient arguments")
                        return
                    if isdigit(temp[-2]) and isdigit(temp[-3]): out = [opRules[opr](temp[-3], temp[-2])+'']+out
                    elif opr == "*":
                        if isDigit(temp[-2]): out = [f"{temp[-2]}{temp[-3]}"] + out
                        else: out = [f"{temp[-3]}{temp[-2]}"] + out
                    if opr in ["+", "-"]: op[0] = op[f"({op[0]})"]



