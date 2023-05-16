# Graciously Computer-Algebra System
# Base classes for individual abstract and specific operators
# Author: Grace Unger
# Created: 5-4-23

import math
import term
import gsymbol

class GOperator(gsymbol.GSymbol):

    OPERATOR_FUNCTIONS={
        "*": lambda x, y: x * y, 
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "/": lambda x, y: x / y,
        "^": lambda x, y: x ** y,
        "sin": lambda x: math.sin(x),
        "cos": lambda x: math.cos(x),
        "tan": lambda x :math.tan(x), 
        "log": lambda x: math.log(x)}
    
    OPERATOR_VALENCE = {
        "*":2, "-":2, "+":2, "/":2, "^":2, 
        "sin":1, "cos":1, "tan":1, "log":1}
    
    OPERATOR_PRECEDENCE = {
        "*":3, "-":2, "+":2, "/":3, "^":4, 
        "sin":5, "cos":5, "tan":5, "log":5}
    
    def __init__(self, label):
        super().__init__(label)
        self.action = self.OPERATOR_FUNCTIONS[self.label]
        self.valence = self.OPERATOR_VALENCE[self.label]
        self.precedence = self.OPERATOR_PRECEDENCE[self.label]

    def act(self, args):
        if not len(args) == self.valence:
            raise Exception(f"Too many arguments passed to operator {self}. \nExpected {self.valence} but {len(args)} arguments were passed: \n{args}") 
        return self.action(*args)