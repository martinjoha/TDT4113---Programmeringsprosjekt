from math import sqrt

e = 0.93
v = 0.0651

for i in range(250,260):
    x = 243 - (0.93 * i)
    print(x)
    y  =sqrt(v * i)
    print(y)
    print(x/y, i)
