from Expression import Expression

# y = Expression("(x+x * y^2)^3")
# print(f"Original expression: {y}")
# y.process()
# print(f"Converted to RPN: {y}")

z = Expression("(x+y)^2 - (4-6)^3")
x = z
x.process()
print(x)
z.evaluate()

print(f"Simplied RPN: {z}")