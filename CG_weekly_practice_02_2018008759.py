import numpy as np
import math

M = np.arange(2, 27, 1)
print(M)

M = M.reshape(5,5)
print(M)

for i in M:
	i[0] = 0
print(M)

M = M@M
print(M)

M_sum = 0
v = M[0]
for i in range(0, 5):
	M_sum = M_sum + math.pow(v[i], 2)
m = np.sqrt(M_sum)
print(m)
