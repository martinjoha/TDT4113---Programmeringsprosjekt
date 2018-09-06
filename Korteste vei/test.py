import math

b1 = 1.5585
t = 2.306

Sxx = 15.28
Sxy = 19.09
Syy = 35.61

n = 10

s2 = (Syy - b1*Sxy)/(n-2)

s = math.sqrt(s2)

lower = (Sxy/Sxx) - t * (s / math.sqrt(Sxx))
upper = b1 + t * (s / math.sqrt(Sxx))

print(lower)
print(upper)
