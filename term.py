# Graciously Computer-Algebra System
# Base classes for individual abstract and numeric terms
# Author: Grace Unger
# Created: 5-4-23
#
# This file should only be accessible by Expressions, Equations, and Operators


import math
import gsymbol
import re

class Term(gsymbol.GSymbol):
    def __init__(self, label):
        super().__init__(label)
        self.equalTerms = [self]
        self.equalExprs = []

    def __str__(self):
        return re.match(r".+\..{0,5}", self.label).group(0)

    def __add__(self, addend):
        return Term(self.label + " + " + addend.label)

    def __sub__(self, subtrahend):
        return Term(self.label + " - " + subtrahend.label)

    def __mul__(self, factor):
        if type(factor) == NumTerm:
            return Term(f"{factor.label}{self.label}")
        return Term(f"{self.label}{factor.label}")

    def __truediv__(self, divisor):
        return Term(self.label + "/" + divisor.label)
    
    def __pow__(self, exponent):
        return Term(self.label + "^" + exponent.label)
    
    def makeTerm(self, label):
        if re.match(r"\d+\.?\d*", label):
            return NumTerm(label)
        if re.match(r"[A-Za-z]", label):
            return VarTerm(label)
        return Term(label)
    
#Purely numeric terms. 
#Rounds tracks up to 1e-10 precision
class NumTerm(Term):
    def __init__(self, label):
        super().__init__(label)
        numVal = float(label)
        if abs(numVal - round(numVal)) < 10 ** -10:
            self.value = round(numVal)
            self.label = f"{self.value}"
        else: self.value = numVal

    def __add__(self, addend):
        return NumTerm(f"{self.value + addend.value}")

    def __sub__(self, subtrahend):
        return NumTerm(f"{self.value - subtrahend.value}")
    
    def __mul__(self, factor):
        return NumTerm(f"{self.value * factor.value}")
    
    def __truediv__(self, divisor):
        return NumTerm(f"{self.value / divisor.value}")
    
    def __neg__(self):
        return NumTerm(f"{self.value * -1}")

    def __pow__(self, exponent):
        return NumTerm(f"{self.value ** exponent.value}")
    

class Constant(NumTerm):
    def __init__(self, label):
        super().__init__(label)


class VarTerm(Term):

    def __init__(self, label):
        super().__init__(label)

#Multiplies two variable terms together. Checks if they have the same base. If they do, then adds the exponents. 
#TODO: A version of this should probably in in NumTerm too because of 3^x type things
    def __mul__(self, factor):
        varRegex = r"^[a-zA-Z]"
        expRegex = r"\^.*"
        base = re.search(varRegex, self.label).group(0)
        factorBase = re.search(varRegex, factor.label).group(0)
        if base == None or factorBase == None:
            raise Exception(f"{self} or {factor} is not an alphabetic variable")
        if base == factorBase:
            exp1, exp2  = re.search(expRegex, self.label).group(0), re.search(expRegex, factor.label).group(0)
            [exp1, exp2] = map(lambda x: 1 if x == None else x[1:], [exp1, exp2])
            expTerm1 = self.makeTerm(exp1)
            expTerm2 = self.makeTerm(exp2)
            newExp = expTerm1 + expTerm2
            if re.match(r"\d+\.0*$"): newExp.label = str(int(newExp.label))
            return Term(f"{base} ^ {newExp.label}")
        return VarTerm(f"{self}{factor}")

#Divides one variable term by another. Essentially the same as __mul__
    def __truediv__(self, divisor):
        varRegex = r"^[a-zA-Z]"
        expRegex = r"\^.*"
        base = re.search(varRegex, self.label).group(0)
        divBase = re.search(varRegex, divisor.label).group(0)
        if base == None or divBase == None:
            raise Exception(f"{self} or {divisor} is not an alphabetic variable")
        if base == divBase:
            exp1 = re.search(expRegex, self.label)
            exp2 = re.search(expRegex, divisor.label)
            [exp1, exp2] = map(lambda x: 1 if x == None else x.group(0)[1:], [exp1, exp2])
            expTerm1 = self.makeTerm(exp1)
            expTerm2 = self.makeTerm(exp2)
            newExp = expTerm1 - expTerm2
            if newExp.label.isnumeric(): newExp.label = int(newExp.label)
            return Term(f"{base} ^ {newExp.label}")
        return VarTerm(f"{self}{divisor}")
