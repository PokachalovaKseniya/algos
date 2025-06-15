# cooding=windows-1251 
import numpy as np

def simpson_rule(f, a, b, n):
    if n % 2 == 1:
        n += 1  
    h = (b - a) / n
    x = np.linspace(a, b, n+1)
    fx = f(x)

    integral = (h / 3) * (fx[0] + 4 * sum(fx[1:-1:2]) + 2 * sum(fx[2:-2:2]) + fx[-1])
    return integral

f1 = lambda x: 6 + 2 * x
f2 = lambda x: 6 - 2 * x
res1 = simpson_rule(f1, -3, 0, 1)
res2 = simpson_rule(f2, 0, 3, 1)
area = res1 + res2
print(area)