# coding=windows-1251
import random
import threading
import time

def quick_sort(array, parall_mode = False, num_flow = 1, min_array_size = 1000):
    if len(array) <= 1:
        return array 

    pivot = array[len(array) // 2]
    left_array = [x for x in array if x < pivot]
    middle_array = [x for x in array if x == pivot]
    right_array = [x for x in array if x > pivot]

    if parall_mode:
        if len(array) > min_array_size and num_flow > 1:
            res = [None] * 2

            def sort_left_array():
                res[0] = quick_sort(left_array, True, num_flow // 2, min_array_size)

            def sort_right_array():
                res[1] = quick_sort(right_array, True, num_flow // 2, min_array_size)
            
            flow1 = threading.Thread(target = sort_left_array)
            flow2 = threading.Thread(target = sort_right_array)

            flow1.start()
            flow2.start()

            flow1.join()
            flow2.join()

            sort_left = res[0]
            sort_right = res[1]
        else:
            sort_left = quick_sort(left_array, False)
            sort_right = quick_sort(right_array, True)
        return sort_left + middle_array + sort_right
    else:
        sort_left = quick_sort(left_array)
        sort_right = quick_sort(right_array)
        return sort_left + middle_array + sort_right

array_1000 = [random.randint(1, 10000) for _ in range(1000)]
array_10000 = [random.randint(1, 10000) for _ in range(10000)]
array_100000 = [random.randint(1, 10000) for _ in range(100000)]

all_array = [array_1000, array_10000, array_100000] 



timings = []

for array in all_array:
    array_size = len(array)

    start_time = time.time()
    quick_sort(array.copy())
    end_time = time.time()

    duration = end_time - start_time
    timings.append((array_size, 1, duration)) 

flow_num = [2, 4, 8]
for flow_size in flow_num:
    for array in all_array:
        array_size = len(array)
        
        start_time = time.time()
        quick_sort(array.copy(), parall_mode = True, num_flow = flow_size, min_array_size = 1000)
        end_time = time.time()

        duration = end_time - start_time
        timings.append((array_size, flow_size, duration))

for res in timings:
    print(f"время: {res}")

for array_size in [len(b) for b in all_array]:
    base_time = 0
    for res in timings:
        if res[0] == array_size and res[1] == 1:
            base_time = res[2]
            break

    for  flow_size in flow_num:
        parall_time = 0
        for res in timings:
            if res[0] == array_size and res[1] == flow_size:
                parall_time = res[2]
                break
        if parall_time > 0:
            speedup = base_time / parall_time
            print(f"количество потоков: {flow_size}. время: {parall_time}. ускорение в {speedup} раз.")