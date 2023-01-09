# Gracious Computer-Algebra
# Author: Grace Unger
# Stores an input string as a list of tokens
# and handles basic operations to manipulate

class Symbol:

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
    def par(term):
        return Symbol(f"({term})")
