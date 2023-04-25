# Graciously Computer-Algebra
# Author: Grace Unger
# Created: 1-8-23
# Modified: 4-24-23
# Stores an input string as a list of tokens
# and evaluates simple expressions according to a Shunting Yard algorithm

import math
import re

# Constants: 
#   OPERATORS: Symbol:Precendence
#   RESERVED_SYMBOLS: Disallowed names of variables
#   OPERATOR_FUNCTIONS: Anonymous functions for each predefined operator
#   OPERATOR_ARGUMENTS: Number of inputs for each predefined operator
class Symbol:

    OPERATORS = {"*":3, "-":2, "+":2, "/":3, "^":4,
                 "sin":5, "cos":5, "tan":5, "log":5}
    RESERVED_SYMBOLS=("*", "-", "+", "/", "sin", "cos", "tan", "(", ")")
    OPERATOR_FUNCTIONS={"*": lambda x, y: x * y, 
             "+": lambda x, y: x + y,
             "-": lambda x , y: x - y,
             "/": lambda x , y: x / y,
             "sin": lambda x: math.sin(x),
             "cos": lambda x:math.cos(x),
             "tan": lambda x :math.tan(x), 
             "log": lambda x:math.log(x)}
    OPERATOR_VALENCE = {"*":2, "-":2, "+":2, "/":2, "^":2,
              "sin":1, "cos":1, "tan":1, "log":1}


    # Takes an input string and tokenizes it into an array of formal symbols and numbers
    # First checks to see if the start of the string is a reserved symbol, which are taken as chunks separately
    # Then checks if it is an alpha character and adds as a single character variable
    # Then takes any chunk of digits and adds them as a single token

    def __init__(self, inputStr = "", inputTokens = []):
        if(inputTokens):
            self.tokens = inputTokens
            return
        self.tokens = []
        inputStr = re.sub(r" ", "", inputStr)
        initialNumRegex = r"^[0-9]*"
        while(inputStr):
            initialSeg = filter(lambda x:inputStr.startsWith(x), self.RESERVED_SYMBOLS)[0]
            if(initialSeg):
                self.tokens += [initialSeg]
                re.sub(rf"^{initialSeg}", "", inputStr)
            elif(re.test(r"^[a-zA-Z]", inputStr[0])):
                self.tokens += inputStr[0]
                inputStr = inputStr[1:]
            elif(re.match(initialNumRegex, inputStr)):
                self.tokens += re.match(initialNumRegex, inputStr)

            

    # Defining formal operations on Symbols. 
    # TODO: Refactor this to not require reassigning into a string
    
    def __str__(self):
        return ''.join(x for x in self.tokens)

    def __add__(self, addend):
        return Symbol(f"{self}+{addend}")

    def __sub__(self, subtrahend):
        return Symbol(f"{self}-{subtrahend}")

    def __mul__(self, factor):
        return Symbol(f"{self}*{factor}")
    
    def __truediv__(self, divisor):
        return Symbol(f"{self}/{divisor}")
    
    def __neg__(self):
        return Symbol(f"-{self}")

    def par(exp):
        return Symbol(f"({exp})")
    

    # Converts a linear arithmetic symbol into Reverse-Polish Notation
    # According to the Shunting-Yard Algorithm
    def linearToRPN(self):
        while(self.tokens):
