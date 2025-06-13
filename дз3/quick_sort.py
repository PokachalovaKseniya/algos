#coding=windows-1251
import random
import unittest
import time

array = []

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} выполнилась за {end_time - start_time:.4f} секунд")
        return result
    return wrapper

@measure_time
def quick_sort(start, end):
    if start >= end:
        return

    pivot = array[end]
    left = start

    for right in range(start, end):
        if array[right] < pivot:
            array[left], array[right] = array[right], array[left]
            left += 1

    array[left], array[end] = array[end], array[left]

    quick_sort(start, left - 1)
    quick_sort(left + 1, end)

class QuickSortTest(unittest.TestCase):
    def test_empty_array(self):
        self.assertEqual(quick_sort([]), [])
    
    def test_single_element(self):
        self.assertEqual(quick_sort([42]), [42])
    
    def test_sorted_array(self):
        self.assertEqual(quick_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])
    
    def test_reverse_sorted(self):
        self.assertEqual(quick_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])
    
    def test_random_array(self):
        test_array = [random.randint(1, 1000) for _ in range(100)]
        self.assertEqual(quick_sort(test_array.copy()), sorted(test_array))
    
    def test_large_numbers(self):
        test_array = [random.randint(1, 10000) for _ in range(100)]
        self.assertEqual(quick_sort(test_array.copy()), sorted(test_array))

if __name__ == '__main__':
    demo_array = [random.randint(1, 100) for _ in range(10)]
    quick_sort(demo_array.copy())
    print(f"Демо-массив до сортировки:{demo_array}")
    print(f"Демо-массив после сортировки: {quick_sort(demo_array.copy())}")
    unittest.main()
