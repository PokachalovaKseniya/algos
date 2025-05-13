# coding=windows-1251 
import unittest
import numpy as np

def simpson_rule(f, a, b, n):
    if n % 2 == 1:
        n += 1  # Делаем n четным
    h = (b - a) / n
    x = np.linspace(a, b, n+1)
    fx = f(x)

    integral = (h / 3) * (fx[0] + 4 * sum(fx[1:-1:2]) + 2 * sum(fx[2:-2:2]) + fx[-1])
    return integral


f1 = lambda x: (3 - x) - (-3 + x) 
f2 = lambda x: (3 + x) - (-3 - x) 

def func(n):
    result1 =simpson_rule(f1, 0, 3, n)
    result2=simpson_rule(f2, -3, 0, n)
    return result1 + result2

for n in range(1,10000,1000):
    print(f"результат для n = {n}: " + str(func(n)))

class TestinFunc(unittest.TestCase):
    def test_func(self):
        self.assertAlmostEqual(func(100), func(1000), places=7)
        self.assertAlmostEqual(func(1000), func(5000), places=7)
        self.assertAlmostEqual(func(5000), func(10000), places=7)
if __name__ == "__main__":
    unittest.main()
