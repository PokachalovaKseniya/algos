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
def radix_sort(array: list) -> list:
    if not array:
        return array
    
    maximum = max(array)
    radix = 1
    while maximum // radix > 0:
        array = sort_by_radix(array, radix)
        radix *= 10
    return array

def sort_by_radix(array: list, radix: int) -> list:
    baskets = [[] for _ in range(10)]
    for num in array:
        digit = (num // radix) % 10
        baskets[digit].append(num)
    
    sorted_array = []
    for basket in baskets:
        sorted_array.extend(basket)
    return sorted_array

class RadixSortTest(unittest.TestCase):
    def test_empty_array(self):
        self.assertEqual(radix_sort([]), [])
    
    def test_single_element(self):
        self.assertEqual(radix_sort([42]), [42])
    
    def test_sorted_array(self):
        self.assertEqual(radix_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])
    
    def test_reverse_sorted(self):
        self.assertEqual(radix_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])
    
    def test_random_array(self):
        array = [random.randint(1, 1000) for _ in range(1000)]
        self.assertEqual(radix_sort(array.copy()), sorted(array))
    
    def test_large_numbers(self):
        self.assertEqual(radix_sort([1000000, 999999, 1000001]), [999999, 1000000, 1000001])

if __name__ == '__main__':
    demo_array = [random.randint(1, 100) for _ in range(1000000)]
    radix_sort(demo_array.copy())
    print(f"Демо-массив до сортировки: ")
    print(f"Демо-массив после сортировки: ")
    unittest.main()


