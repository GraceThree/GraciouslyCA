# Graciously Computer-Algebra System
# Base classes for all abstract symbols
# Author: Grace Unger
# Created: 5-4-23

# Should be essentailly invisible to everything else


class GSymbol:
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return self.label
    
class paren(GSymbol):
    def __init__(self, label):
        super().__init__(label)
        if self.label == "(":
            self.side = "l"
        else:
            self.side = "r"