# Graciously Computer-Algebra System
# Base class to manipulate Symbolic Expressions
# Author: Grace Unger
# Created: 1-8-23
# Modified: 4-25-23
# Stores an input string as a list of tokens
# and evaluates simple expressions according to a Shunting Yard algorithm

import math
import re
from queue import LifoQueue, Queue

# TODO: Implement SYA
# TODO: Refactor formal operations to allow for mixed String and [token] inputs
# TODO: Add check in token input for __init__ that only valid tokens are passed
# TODO: Account for 2x type tokens with implicit multiplication
# TODO: [long-term] make a front-end UI in JS with:
#               LaTeX integration
#               Basic 2d graphing capabilities
#               Easy system of eqn input
#               

# Constants: 
#   OPERATORS: Symbol:Precendence, used for Shunting Yard 
#   RESERVED_SYMBOLS: Strings to be tokenized independently
#   OPERATOR_FUNCTIONS: Anonymous functions for each predefined operator
#   OPERATOR_ARGUMENTS: Number of inputs for each predefined operator

class Expression:

    OPERATORS = {"*":3, "-":2, "+":2, "/":3, "^":4}
    FUNCTIONS = {"sin":5, "cos":5, "tan":5, "log":5}
    RESERVED_SYMBOLS=("*", "-", "+", "/", "sin", "cos", "tan", "(", ")", "log")
    OPERATOR_FUNCTIONS={"*": lambda x, y: x * y, 
             "+": lambda x, y: x + y,
             "-": lambda x , y: x - y,
             "/": lambda x , y: x / y,
             "sin": lambda x: math.sin(x),
             "cos": lambda x: math.cos(x),
             "tan": lambda x :math.tan(x), 
             "log": lambda x: math.log(x)}
    OPERATOR_VALENCE = {"*":2, "-":2, "+":2, "/":2, "^":2}
    FUNCTION_VALENCE ={"sin":1, "cos":1, "tan":1, "log":1}
    


    # Takes an input string and tokenizes it into a Queue of formal symbols and numbers
    # First checks to see if the start of the string is a reserved symbol, which are taken as chunks separately
    # Then checks if it is an alpha character and adds as a single character variable
    # Then takes any chunk of digits and adds them as a single token
    # Ignores any other characters
    # If a preexisting list of tokens is passed, then any new tokens are appended

    def __init__(self, inputStr = "", inputTokens = Queue(0)):
        self.tokens = inputTokens
        inputStr = re.sub(r" ", "", inputStr)
        initialNumRegex = r"^\d*\.?\d*"
        while(inputStr):
            initialSeg = filter(lambda x: inputStr.startsWith(x), 
                                self.RESERVED_SYMBOLS)
            if(initialSeg):
                self.tokens.put(initialSeg[0])
                re.sub(rf"^{initialSeg[0]}", "", inputStr)
            elif(re.match(r"^[a-zA-Z]", inputStr[0])):
                self.tokens.put(inputStr[0])
                inputStr = inputStr[1:]
            elif(re.match(initialNumRegex, inputStr)):
                self.tokens.put(re.match(initialNumRegex, inputStr))
                re.sub(initialNumRegex, "", inputStr)
            else:
                raise Exception("Invalid character in input string.")
                break
            

    # Defining formal operations on Expressions. tempOp
        return Expression(f"{self}+{addend}")

    def __sub__(self, subtrahend):
        return Expression(f"{self}-{subtrahend}")

    def __mul__(self, factor):
        return Expression(f"{self}*{factor}")
    
    def __truediv__(self, divisor):
        return Expression(f"{self}/{divisor}")
    def __neg__(self):
        return Expression(f"-{self}")

    def par(exp):
        return Expression(f"({exp})")    

    # Converts a linear arithmetic Expression into Reverse-Polish Notation
    # According to the Shunting-Yard Algorithm
    def linearToRPN(self):
        opStack = LifoQueue(0)
        outQueue = Queue(0)
        while(not self.tokens.empty()):
            token = self.tokens.get()
            if re.match(r"^\d*\.?\d*|^[A-Za-z]", token): 
                outQueue.put(token)
            elif token in self.FUNCTIONS.keys():
                opStack.put(token)
            elif token in self.OPERATORS.keys():
                tempOp = opStack.get()
                while(tempOp in self.OPERATORS.keys() and not tempOp == "(" 
                      and self.OPERATORS(tempOp)>self.OPERATORS):
                    outQueue.put(tempOp)
                    tempOp = opStack.get()
                opStack.put(token)
            elif token == "(":
                outQueue.put(opStack.get())
            elif token == ")":
                tempOp = opStack.get()
                while(not tempOp == "("):
                    if not opStack.empty():
                        outQueue.push(tempOp)
                        tempOp = opStack.get()
                    else:
                        raise Exception("Mismatched parentheses!")
            
            while(not opStack.empty()):
                tempOp = opStack.get()
                if tempOp ==  "(" or tempOp == ")":
                    raise Exception("Mismatched parentheses!")
                outQueue.put(opStack.get)

        self.tokens = outQueue

