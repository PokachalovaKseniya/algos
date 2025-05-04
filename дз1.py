# coding=windows-1251  
import random
import time

def bb_element(arr):
    if not arr:  
        print("Ошибка: список пуст!")
        return arr  
    rand_el = random.randrange(len(arr))
    b_el = arr.pop(rand_el)
    print(f"Удален элемент {b_el} (индекс: {rand_el})")
    return arr

# Генерация списка из 1000 случайных чисел
ans = [random.randint(1, 10) for _ in range(1000000)]
print("Массив до удаления:", ans)

start_time = time.time()  
ans = bb_element(ans)
end_time = time.time()    

print("Массив после удаления:", ans)
exec_time = end_time - start_time  
print(f"Время выполнения: {exec_time} с")
