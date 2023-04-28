from Expression import Expression

# Unit tests for numerical expression inputs
# Currently: Tests RPN conversion and evaluation separately 
# Note: Requires 1 trailing space in test strings. 
def testNums():
    numTest = Expression("(11+1)^2 - 4")
    numTestTwo = Expression("(11+1)^2 - 4")

    numTest.process()
    assert str(numTest) == "11 1 + 2 ^ 4 - "

    numTestTwo.evaluate()
    print(f"numTestTwo evaluates to {str(numTestTwo)}")
    assert str(numTestTwo) == "140 "


# Unit tests for basic symbolic inputs with no numeric simplification needed
# Currently: Tests processing into RPN and that evaluation doesn't change anything
def testSymb():
    varTest = Expression("(x+y)^2 + 3")
    varTestTwo = Expression("(x+y)^2 + 3")

    varTest.process()
    assert str(varTest) == "x y + 2 ^ 3 + "

    varTestTwo.evaluate()
    assert str(varTestTwo) == "x y + 2 ^ 3 "

testNums()
#testSymb()