# Graciously Computer-Algebra System
# Base classes for individual abstract and numeric terms
# Author: Grace Unger
# Created: 5-4-23
#
# This file should only be accessible by Expressions, Equations, and Operators


import math
import gsymbol
import re
from expression import Expression

#   label - string representation of the term. Potentially more complicated than a single symbol. This is parsed out as needed when evaluated as an Expression
#   equalTerms - all other known terms equal to this. Used for simplification rules
#   equalExprs - all expressions or values equal to this
class Term(gsymbol.GSymbol):
    def __init__(self, label):
        super().__init__(label)
        self.equalExprs = {self.label}
        self.value = None

    def __str__(self):
        return re.match(r".+\.?.{0,5}", self.label).group(0)

    def __add__(self, addend):
        return Term(self.label + " + " + addend.label)

    def __sub__(self, subtrahend):
        return Term(self.label + " - " + subtrahend.label)

#Multiplies two abstract terms together. Checks to see if two have the same base, and adds the exponents in this case. Currently cannot handle exponents contained within parens, so 
#TODO: Add handling for stuff like (x^2+3) * x, currently should output x ^ 6
#TODO: Cleanly support outputting directly as Expression
    def __mul__(self, factor):
        expRegex = r"\^.*"
        base = re.search(r"^.*\^?", self.label).group(0)
        factorBase = re.search(r"^.*\^?", factor.label).group(0)
        if base == None or factorBase == None:
            raise Exception(f"Okay what the hell grace how, mul version")
        #If bases are equal, inserts a dummy exponent of 1 if exp is blank,
        if base == factorBase:
            exp1 = re.search(expRegex, self.label).group(0)
            exp2 = re.search(expRegex, factor.label).group(0)
            [exp1, exp2] = map(lambda x: 1 if x == None else x[1:], [exp1, exp2])
            expTerm1 = self.__makeTerm(exp1)
            expTerm2 = self.__makeTerm(exp2)
            newExp = expTerm1 + expTerm2
            if re.match(r"^\d+\.?0*$", newExp.label): newExp.label = str(int(newExp.label))
            if re.match(r"^1\.?0*$", newExp.label): return Term(f"{base}")
            return Expression(f"{base} ^ {newExp.label}")
        if type(factor) == NumTerm: return Term(f"{factor}{self}")
        return Term(f"{self}{factor}")

    def __truediv__(self, divisor):
        expRegex = r"\^.*"
        base = re.search(r"^.*\^?", self.label).group(0)
        divBase = re.search(r"^.*\^?", divisor.label).group(0)
        if base == None or divBase == None:
            raise Exception(f"Okay what the hell grace how")
        if base == divBase:
            exp1 = re.search(expRegex, self.label)
            exp2 = re.search(expRegex, divisor.label)
            [exp1, exp2] = map(lambda x: 1 if x == None else x.group(0)[1:], [exp1, exp2])
            expTerm1 = self.__makeTerm(exp1)
            expTerm2 = self.__makeTerm(exp2)
            newExp = expTerm1 - expTerm2
            if re.match(r"^\d+\.?0*$", newExp.label): newExp.label = str(int(newExp.label))
            if re.match(r"^1\.?0*$", newExp.label): return Term(f"{base}")
            return Term(f"{base} ^ {newExp.label}")
        return Term(f"{self} / {divisor}")
    
    def __pow__(self, exponent):
        return Term(self.label + " ^ " + exponent.label)
    
    #Helper function for VarTerm.__mul__ and VarTerm.__div__, here because it could be useful elsewhere
    def __makeTerm(self, label):
        if re.match(r"\d+\.?\d*", label):
            return NumTerm(label)
        if re.match(r"[A-Za-z]", label):
            return VarTerm(label)
        return Term(label)
    
    #Two terms are equal their label is in the others list of equal expressions. Somewhat crude, and TODO:probably should make this less stupid
    def __eq__(self, other):
        if other.label in self.equalExprs or self.label in other.equalExprs:
            self.equalExprs.add(other.label)
            other.equalExprs.add(self.label)
            return True
        return False
    
#Purely numeric terms. 
#Tracks up to 1e-10 precision
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
        if self.value == factor.value: return Term(f"{self} ^ 2")
        return NumTerm(f"{self.value * factor.value}")
    
    def __truediv__(self, divisor):
        return NumTerm(f"{self.value / divisor.value}")
    
    def __neg__(self):
        return NumTerm(f"{self.value * -1}")

    #Checks if self ** exponent < 10^6, otherwise makes into a single term self ^ exponent
    def __pow__(self, exponent):
        if exponent.value * math.log(self.value, 10) < 7:
           return NumTerm(f"{self.value ** exponent.value}")
        return Term(f"{self.value} ^ {exponent.value}")  

class Constant(NumTerm):
    CONSTANTS = {"e": math.e, "pi": math.pi}

    def __init__(self, label):
        self.label = label
        self.value = self.CONSTANTS[self.label]

class VarTerm(Term):
    def __init__(self, label):
        super().__init__(label)