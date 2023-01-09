# contains current tests for CA system


x = ca.Symbol("x")
y = ca.Symbol("y")

print(x+y)
print(x-y)

exp1 = ca.Symbol("(2*4)+6")
print(exp1)
print(ca.par(x+y)*exp1)


