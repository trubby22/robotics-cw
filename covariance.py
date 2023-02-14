import math

# Measurements of robot going around the square for previous lab
n = 10
xs = [
    -0.3,
    -1.7,
    0.4,
    -0.5,
    -0.7,
    -1.9,
    -1.1,
    -2.0,
    0.6,
    -1.9,
]
ys = [
    3.5,
    0.5,
    1.4,
    0.7,
    -0.4,
    1.8,
    1.1,
    0.6,
    -1.5,
    0.7,
]
x_mean = 1/n * sum(xs)
y_mean = 1/n * sum(ys)
top_left = 1/n * sum([(x - x_mean) ** 2 for x in xs])
bottom_right = 1/n * sum((y - y_mean) ** 2 for y in ys)
foo = [x - x_mean for x in xs]
bar = [y - y_mean for y in ys]
top_right = 1 / n * sum([f * b for f, b in zip(foo, bar)])
print(f"Top left: {top_left}")
print(f"Top right: {top_right}")
print(f"Bottom right: {bottom_right}")

print(f"Standard deviation - x: {math.sqrt(top_left)}")
print(f"Standard deviation - y: {math.sqrt(bottom_right)}")
