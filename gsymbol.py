# Graciously Computer-Algebra System
# Base classes for all abstract symbols
# Author: Grace Unger
# Created: 5-4-23

# Contains a few methods that are universal to all symbolic objects. Also contains parens since they work differently and don't need any of the structure of Operators or Terms

class GSymbol:
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return self.label
    
class Paren(GSymbol):
    def __init__(self, label):
        super().__init__(label)
        if self.label == "(":
            self.side = "l"
        else:
            self.side = "r"