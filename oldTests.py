from expression import Expression

# Unit tests for numerical expression inputs
# Currently: Tests RPN conversion and evaluation separately 
# Note: Requires 1 trailing space in test strings. 

# Functions as of 5:32 PM 4/28/23
def testNums():
    numTest = Expression("(11+1)^2 - x")
    numTestTwo = Expression("(11+1)^2 - x")

    numTest.process()
    assert str(numTest) == "11 1 + 2 ^ x - "

    numTestTwo.evaluate()
    print(f"numTestTwo evaluates to {str(numTestTwo)}")
    assert str(numTestTwo) == "144 x - "

# Unit tests for basic symbolic inputs with no numeric simplification needed
# Currently: Tests processing into RPN and that evaluation doesn't change anything
def testSymb():
    varTest = Expression("(x+y)^2 + 3")
    varTestTwo = Expression("(x+y)^2 + 3")

    varTest.process()
    print(varTest)
    assert str(varTest) == "x y + 2 ^ 3 + "
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    varTestTwo.evaluate()
    print(varTestTwo)
    assert str(varTestTwo) == "x y + 2 ^ 3 "

#testNums()
testSymb()