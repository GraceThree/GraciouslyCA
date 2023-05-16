# Graciously Computer-Algebra System
# Base class to manipulate Symbolic Expressions
# Author: Grace Unger
# Created: 1-8-23
# Stores an input string as a list of tokens
# and evaluates simple expressions according to a Shunting Yard algorithm

import math
import re
from collections import deque
from goperator import GOperator
from term import Term, VarTerm, NumTerm, Constant
from gsymbol import GSymbol, Paren
import copy

# TODO: Complete refector - treating it as a str list is actually really annoying, when instead we could really OOP it up into terms and operators, and have the expression input just parse that

# TODO: Refactor formal operations to allow for mixed String and [token] inputs
# TODO: [long-term] make a front-end UI in JS with:
#               LaTeX integration
#               Basic 2d graphing capabilities
#               Easy system of eqn input
#               

# Constants: 
#   OPERATORS: Symbol:Precendence, used for Shunting Yard 
#   RESERVED_SYMBOLS: Strings to be tokenized independently
#   FUNCTION_CALLS: Anonymous functions for each predefined operator
#   OPERATOR_ARGUMENTS: Number of inputs for each predefined operator

class Expression:
    RESERVED_SYMBOLS=("*", "-", "+", "/", "^", "(", ")",
                      "sin", "cos", "tan", "log", "pi", "e")

    # Takes an input string and tokenizes it into a Queue of GSymbols 
    # First checks to see if the start of the string is a reserved symbol, which are taken as chunks separately, turned into either operators, parens, or constants
    # Then checks if it is an alpha character or number-alpha product to treat as a variable or unit term
    # Then takes any chunk of digits and adds them as a single token
    # Ignores any other characters
    # If a preexisting list of tokens is passed, then any new tokens are appended

    def __init__(self, inputStr:str = "", inputTokens:deque = deque()):
        self.tokens = deque() + inputTokens
        inputStr = re.sub(r"\s", "", inputStr)
        inputStr = re.sub(r"^\-", "0-", inputStr)
        initialNumRegex = r"^\d+\.?\d*"
        numVarRegex = r"^\d*\.?\d*[a-zA-Z]?"
        while(inputStr):
            initialSeg = list(filter(lambda x: inputStr.startswith(x), self.RESERVED_SYMBOLS))
            if(initialSeg):
                if initialSeg[0] in GOperator.OPERATOR_FUNCTIONS.keys():
                    self.tokens.append(GOperator(initialSeg[0]))
                elif initialSeg[0] in Constant.CONSTANTS.keys():
                    self.tokens.append(Constant(initialSeg[0]))
                elif initialSeg[0] in ["(", ")"]:
                    self.tokens.append(Paren(initialSeg))
                else:
                    raise Exception("Somehow this is a reserved symbol but not some kind of reserved symbol. You've fucked up grace.")
                inputStr = inputStr[1:]
            elif(re.match(numVarRegex, inputStr)):
                self.tokens.append(Term(re.search(numVarRegex, inputStr).group(0)))
                inputStr = re.sub(numVarRegex, "", inputStr)
            elif(re.match(initialNumRegex, inputStr)):
                self.tokens.append(NumTerm(re.match(initialNumRegex, inputStr).group(0)))
                inputStr = re.sub(initialNumRegex, "", inputStr)
            else:
                raise Exception(f"Invalid character {inputStr[0]} in input string.")
        #self.process

    def __repr__(self):
        out = ""
        newQueue= copy.deepcopy(self.tokens)
        while newQueue:
            token = newQueue.popleft()
            out+= f"{str(token)} "
        return out[:-1]

    # Defining formal operations on Expressions

    def __add__(self, addend):
        out = copy.deepcopy(self.tokens)
        out.append(GOperator("+"))
        return Expression(inputTokens=(out + addend.tokens))

    def __sub__(self, subtrahend):
        return Expression(f"{self} - {subtrahend}")

    def __mul__(self, factor):
        return Expression(f"({self}) * ({factor})")
    
    def __truediv__(self, divisor):
        return Expression(f"({self}) / ({divisor})")
    
    def __neg__(self):
        return Expression(f"-({self})")
    
    def __pow__(self, exponent):
        return Expression(f"({self}) ^ {exponent}")

    def par(expr):
        return Expression(f"({expr})")

    def evaluate(self):
        self.__evaluateRPN()

    def process(self):
        self.__linearToRPN()

    def __stackToStr(self, stackToPrint):
        temp = deque()
        out = ""
        while stackToPrint:
               token = stackToPrint.popleft()
               out += token
               temp.append(token)
        stackToPrint = temp
        return out

    def __evaluateRPN(self): 
        #TODO: Rebuild about new symbol implementation
        evalStack = deque()
        outQueue = deque()

        while not len(self.tokens) == 0:
            token = self.tokens.popleft()

            if not token in self.RESERVED_SYMBOLS:
                evalStack.append(token)
            elif bool(re.match(r"\s", token)):
                continue
            else:
                args = ""
                for i in range(0, self.OPERATOR_VALENCE[token]):

                    if evalStack:
                        args += evalStack.popleft()

                    else:
                        raise Exception(f"Insufficient arguments for token {token}. \nArguments supplied: {args[::-1]}")
                    
                args = args[::-1]
                #Check for any elements which have no nested weirdness and are floats
                if(all(type(x) == str for x in args)
                    and all(bool(re.match("^\d+\.?\d*", y)) for y in args)):
                   eval = self.FUNCTION_CALLS[token](*list(map(lambda x: float(x), args)))
                   evalStack.append(eval)

                else:
                    continue
                    # How do I write this in a way that doesn't have weird reversing issues? I can't reverse at each step obvious or weirdness ensues. The nested set approach is probably the best one tbqph
        
        bounceStack = deque()
        newTokens = ""
        while evalStack:
            temp = evalStack.popleft()
            newTokens = temp + newTokens

        self = Expression(newTokens)

        outQueue = self.__cleanNums(self.tokens)

        self.tokens = outQueue
        print(f"Expression after evaluation: {self}")

    # Converts a linear infix Expression into Reverse-Polish Notation
    # According to the Shunting-Yard Algorithm
    def __linearToRPN(self):
        opStack = deque()
        outQueue = deque()
        while self.tokens:
            token = self.tokens.popleft()
            if issubclass(type(token), Term):
                outQueue.append(token)

            elif token in GOperator.FUNCTIONS:
                opStack.append(token)
            elif token in GOperator.OPERATORS:
                if opStack:
                    tempOp = opStack.popleft()
                    while(tempOp in GOperator.OPERATORS): 
                        if(not tempOp == "("
                             and (GOperator.OPERATOR_PRECEDENCE[token]<GOperator.OPERATOR_PRECEDENCE[tempOp] 
                             or (GOperator.OPERATOR_PRECEDENCE[tempOp] == GOperator.OPERATOR_PRECEDENCE[token] and GOperator.OPERATOR_ASSOC[token] == "l"))
                            and opStack):
                            outQueue.append(tempOp)
                            opStack.append(token)
                            break
                        else:
                            outQueue.append(tempOp)
                            if opStack:
                                tempOp = opStack.popleft()
                            else:
                                break
                    if type(tempOp) == Paren:
                        opStack.append(tempOp)
                opStack.append(token)

            elif type(token) == Paren:
                if token.side == "l":
                    opStack.append(token)
                else:
                    tempOp = opStack.popleft()
                    while not type(tempOp == Paren) and tempOp.side == "l":
                        if opStack:
                            outQueue.append(tempOp)
                            tempOp = opStack.popleft()
                        else:
                            raise Exception("Mismatched parentheses!")
                        
                    if opStack:
                        tempOp = opStack.popleft()
                        if tempOp in GOperator.OPERATORS.keys():
                            outQueue.append(tempOp)
                        else:
                            opStack.append(tempOp)
            
        while opStack:
            tempOp = opStack.popleft()
            if type(tempOp == Paren):
                raise Exception("Mismatched parentheses!")
            outQueue.append(tempOp)
        self.tokens = outQueue

    def __cleanNums(self, q: deque):
        newQ = deque()
        while q:
            temp = q.popleft()
            print(f"temp is {temp} in __cleanNums")
            if bool(re.match(r"^\d+\.?0*", temp)):
                newQ.append(str(int(float(temp))))
            else:
                newQ.append(temp)
        return newQ

