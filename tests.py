from Expression import Expression

y = Expression("(x+x * y^2)^3")
print(f"Original expression: {y}")
Expression.simplify(y)
print(f"Converted to RPN: {y}")

#Expression.evaluate(y)

