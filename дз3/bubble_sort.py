# coding=windows-1251
import random
import unittest
import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} выполнилась за {end_time - start_time:.4f} секунд")
        return result
    return wrapper

@measure_time
def bubble_sort(array):
    n = len(array)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array

class BubbleSortTest(unittest.TestCase):
    def test_empty_array(self):
        self.assertEqual(bubble_sort([]), [])
    
    def test_single_element(self):
        self.assertEqual(bubble_sort([42]), [42])
    
    def test_sorted_array(self):
        self.assertEqual(bubble_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])
    
    def test_reverse_sorted(self):
        self.assertEqual(bubble_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])
    
    def test_random_array(self):
        test_array = [random.randint(1, 1000) for _ in range(100)]
        self.assertEqual(bubble_sort(test_array.copy()), sorted(test_array))

if __name__ == '__main__':
    demo_array = [random.randint(1, 100) for _ in range(50000)]
    bubble_sort(demo_array.copy())
    print(f"Демо-массив до сортировки: ")
    print(f"Демо-массив после сортировки: ")
    unittest.main()
