import math
import statistics
import numpy as np

### straight line
a = np.array([200] * 10)
b = np.array([203, 201, 201, 202, 204, 204, 200, 204, 201, 201])
c = np.array([14,  12,  15,  15,  1,   -2,  -36, 1,   11, 4])

# cosin rule
gamma = np.arccos((a**2 + b**2 - c**2) / (2 * a * b)) * 180 / math.pi
#remove nan
gamma = gamma[~np.isnan(gamma)]
print("gamma: ", gamma)
std = statistics.stdev(gamma) / 2
print("std: ", std)


#stdev of b
stdb = statistics.stdev(b - 200) / 20

print("stdb: ", stdb)

### roatation
radius = 10.5
d = 8.9

# cosin rule
res = (np.arccos((radius**2 + radius**2 - d**2) / (2 * radius * radius)) * 180 / math.pi) / 20
print("res: ", res)