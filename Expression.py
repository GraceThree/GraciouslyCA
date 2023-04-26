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
#   FUNCTION_CALLS: Anonymous functions for each predefined operator
#   OPERATOR_ARGUMENTS: Number of inputs for each predefined operator

class Expression:

    OPERATORS = {"*":3, "-":2, "+":2, "/":3, "^":4}
    FUNCTIONS = {"sin":5, "cos":5, "tan":5, "log":5}
    RESERVED_SYMBOLS=("*", "-", "+", "/", "^", "(", ")",
                      "sin", "cos", "tan", "log")
    FUNCTION_CALLS={
             "*": lambda x, y: x * y, 
             "+": lambda x, y: x + y,
             "-": lambda x , y: x - y,
             "/": lambda x , y: x / y,
             "^": lambda x, y: x ** y,
             "sin": lambda x: math.sin(x),
             "cos": lambda x: math.cos(x),
             "tan": lambda x :math.tan(x), 
             "log": lambda x: math.log(x)}
    #TODO: Add exp, refactor some other stuff to make it work bc it's a little weird
    OPERATOR_VALENCE = {"*":2, "-":2, "+":2, "/":2, "^":2, 
                        "sin":1, "cos":1, "tan":1, "log":1}
    OPERATOR_ASSOC = {"*":"l", "-":"l", "+":"l", "/":"l", "^":"r"}

    # Takes an input string and tokenizes it into a Queue of formal symbols and numbers
    # First checks to see if the start of the string is a reserved symbol, which are taken as chunks separately
    # Then checks if it is an alpha character or number-alpha character #product
    # Then takes any chunk of digits and adds them as a single token
    # Ignores any other characters
    # If a preexisting list of tokens is passed, then any new tokens are appended

    def __init__(self, inputStr):
        self.tokens = Queue()
        inputStr = re.sub(r"\s", "", inputStr)
        inputStr = re.sub(r"^\-", "0 - ", inputStr)
        initialNumRegex = r"^\d+\.?\d*"
        while(inputStr):
            initialSeg = list(filter(lambda x: inputStr.startswith(x), 
                                    self.RESERVED_SYMBOLS))
            if(initialSeg):
                self.tokens.put(initialSeg[0])
                inputStr = re.sub(rf"^{re.escape(initialSeg[0])}", "", inputStr)
            elif(re.match(r"^\d*\.?\d*[a-zA-Z]", inputStr[0])):
                self.tokens.put(inputStr[0])
                inputStr = inputStr[1:]
            elif(re.match(initialNumRegex, inputStr)):
                self.tokens.put(re.match(initialNumRegex, inputStr).group(0))
                inputStr = re.sub(initialNumRegex, "", inputStr)
            else:
                raise Exception(f"Invalid character {inputStr[0]} in input string.")

    def __str__(self):
        newQueue = Queue(0)
        out = ""
        while(not self.tokens.empty()):
            token = self.tokens.get()
            out+= token + " "
            newQueue.put(token)
        self.tokens = newQueue
        return out

    # Defining formal operations on Expressions

    def __add__(self, addend):
        return Expression(f"{self} {addend} +")

    def __sub__(self, subtrahend):
        return Expression(f"{self} {subtrahend} -")

    def __mul__(self, factor):
        return Expression(f"{self} {factor} *")
    
    def __truediv__(self, divisor):
        return Expression(f"{self} {divisor} /")
    
    def __neg__(self):
        return Expression(f"-{self}")
    
    def __pow__(self, exponent):
        return Expression(f"{self} {exponent} ^")

    def par(exp):
        return Expression(f"({exp})")

    def evaluate(self):
        self.__linearToRPN()
        self.__evaluateRPN()

    def process(self):
        self.__linearToRPN()
    
    def __evaluateRPN(self):
        evalStack = LifoQueue()
        outQueue = Queue()
        while(not self.tokens.empty()):
            token = self.tokens.get()
            if(token in self.OPERATORS.keys()):
                args = []
                for i in range(0,self.OPERATOR_VALENCE[token]):
                    if (not evalStack.empty()):
                        topStack = evalStack.get()
                        args.append(topStack)
                    else:
                        raise Exception(f"Insufficiant arguments for operator {token}. \nSupplied arguments: {args}, but it required {self.OPERATOR_VALENCE[token]}")
                if(all(x.isnumeric() for x in args)):
                    print(args)
                    eval = str(self.FUNCTION_CALLS[token](*list(map(lambda x: float(x),args))))
                    evalStack.put(eval)
                else:
                    eval = self.FUNCTION_CALLS[token](*list(map(lambda x: Expression(x), args)))
                    outQueue.put(eval)
            else: 
                evalStack.put(token)
        self.tokens = outQueue

    # Converts a linear infix Expression into Reverse-Polish Notation
    # According to the Shunting-Yard Algorithm
    def __linearToRPN(self): #TODO: Fix this... something doesn't work and I'm not sure what
        opStack = LifoQueue(0)
        outQueue = Queue(0)
        while(not self.tokens.empty()):
            token = self.tokens.get()
            if re.match(r"^\d+\.?\d*|^\d*\.?\d*[a-zA-Z]", token): 
                outQueue.put(token)

            elif token in self.FUNCTIONS.keys():
                opStack.put(token)

            elif token in self.OPERATORS.keys():
                if not opStack.empty():
                    tempOp = opStack.get()
                    while(tempOp in self.OPERATORS.keys() 
                        and not tempOp == "("
                             and (self.OPERATORS[tempOp]>self.OPERATORS[token] 
                             or (self.OPERATORS[tempOp] == self.OPERATORS[token] and self.OPERATOR_ASSOC[token] == "l"))
                        and not opStack.empty()):
                        outQueue.put(tempOp)
                        tempOp = opStack.get()
                    else:
                        opStack.put(tempOp)
                opStack.put(token)

            elif token == "(":
                opStack.put(token)

            elif token == ")":
                tempOp = opStack.get()
                while(not tempOp == "("):
                    if not opStack.empty():
                        outQueue.put(tempOp)
                        tempOp = opStack.get()
                    else:
                        raise Exception("Mismatched parentheses!")
                    
                if not opStack.empty():
                    tempOp = opStack.get()
                    if tempOp in self.FUNCTIONS.keys():
                        outQueue.put(tempOp)
                    else:
                        opStack.put(tempOp)
            
        while(not opStack.empty()):
            tempOp = opStack.get()
            if tempOp ==  "(" or tempOp == ")":
                raise Exception("Mismatched parentheses!")
            outQueue.put(tempOp)

        self.tokens = outQueue

