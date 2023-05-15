# Graciously Computer-Algebra System
# Base class to manipulate Symbolic Expressions
# Author: Grace Unger
# Created: 1-8-23
# Stores an input string as a list of tokens
# and evaluates simple expressions according to a Shunting Yard algorithm

import math
import re
from queue import LifoQueue, Queue


# TODO: Complete refector - treating it as a str list is actually really annoying, when instead we could really OOP it up into terms and operators, and have the expression input just parse that

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
    CONSTANTS = {"pi", "e"}
    RESERVED_SYMBOLS=("*", "-", "+", "/", "^", "(", ")",
                      "sin", "cos", "tan", "log")
    FUNCTION_CALLS={
             "*": lambda x, y: x * y, 
             "+": lambda x, y: x + y,
             "-": lambda x, y: x - y,
             "/": lambda x, y: x / y,
             "^": lambda x, y: x ** y,
             "sin": lambda x: math.sin(x),
             "cos": lambda x: math.cos(x),
             "tan": lambda x :math.tan(x), 
             "log": lambda x: math.log(x)}
    #TODO: Add exp, refactor some other stuff to make it work bc it's a little weird
    OPERATOR_VALENCE = {"*":2, "-":2, "+":2, "/":2, "^":2, 
                        "sin":1, "cos":1, "tan":1, "log":1}
    OPERATOR_ASSOC = {"*":"l", "-":"l", "+":"l", "/":"l", "^":"r"}

    # Takes an input string and tokenizes it into a Queue of GSymbols 
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

    def tempStackPrint(self, stackToPrint):
        temp = Queue()
        out = ""
        while(not stackToPrint.empty()):
               token = stackToPrint.get()
               out += token
               temp.put(token)
    
    def __evaluateRPN(self): 
        #TODO: Nope this doesn't work, but you can fix it since you have the proper toRPN implementation now ^_^
        # The issues currently come from how youhandle symbolic expressions, because there's no build in good way to handle the number of args
        evalStack = LifoQueue()
        outQueue = Queue()

        while not(self.tokens.empty()):
            token = self.tokens.get()

            if not token in self.RESERVED_SYMBOLS:
                evalStack.put(token)
            elif bool(re.match(r"\s", token)):
                continue
            else:
                args = ""
                for i in range(0, self.OPERATOR_VALENCE[token]):

                    if(not evalStack.empty()):
                        args += evalStack.get()

                    else:
                        raise Exception(f"Insufficient arguments for token {token}. \nArguments supplied: {args[::-1]}")
                    
                args = args[::-1]
                print(f"args for {token} are {args}")                
                #Check for any elements which have no nested weirdness and are floats
                if(all(type(x) == str for x in args)
                    and all(bool(re.match("^\d+\.?\d*", y)) for y in args)):
                   eval = self.FUNCTION_CALLS[token](*list(map(lambda x: float(x), args)))
                   evalStack.put(eval)

                else:
                    continue
                    # How do I write this in a way that doesn't have weird reversing issues? I can't reverse at each step obvious or weirdness ensues. The nested set approach is probably the best one tbqph
        
        bounceStack = LifoQueue()
        newTokens = ""
        while(not evalStack.empty()):
            temp = evalStack.get()
            newTokens = temp + newTokens

        self = Expression(newTokens)

        outQueue = self.__cleanNums(self.tokens)

        self.tokens = outQueue
        print(f"Expression after evaluation: {self}")

    # Converts a linear infix Expression into Reverse-Polish Notation
    # According to the Shunting-Yard Algorithm
    def __linearToRPN(self):
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
                    while(tempOp in self.OPERATORS.keys()): 
                        if(not tempOp == "("
                             and (self.OPERATORS[token]<self.OPERATORS[tempOp] 
                             or (self.OPERATORS[tempOp] == self.OPERATORS[token] and self.OPERATOR_ASSOC[token] == "l"))
                            and not opStack.empty()):
                            outQueue.put(tempOp)
                            opStack.put(token)
                            break
                        else:
                            outQueue.put(tempOp)
                            if not opStack.empty():
                                tempOp = opStack.get()
                            else:
                                break
                    if(tempOp == "(" or tempOp == ")"):
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

    def __cleanNums(self, q: Queue):
        newQ = Queue()
        while not q.empty():
            temp = q.get()
            print(f"temp is {temp} in __cleanNums")
            if bool(re.match(r"^\d+\.?0*", temp)):
                newQ.put(str(int(float(temp))))
            else:
                newQ.put(temp)
        return newQ

