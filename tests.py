from Expression import Expression

# Unit tests for numerical expression inputs
# Currently: Tests RPN conversion and evaluation separately 
def testNums():
    numTest = Expression("(1+1)^2 - 4")
    numTestTwo = Expression("(1+1)^2 - 4")

    numTest.process()
    assert str(numTest) == "1 1 + 2 ^ 4 - "

    numTestTwo.evaluate()
    assert numTestTwo.tokens == "0"


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