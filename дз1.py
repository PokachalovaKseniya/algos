# coding=windows-1251  
import random
import time

def bb_element(arr):
    if not arr:  
        print("������: ������ ����!")
        return arr  
    rand_el = random.randrange(len(arr))
    b_el = arr.pop(rand_el)
    print(f"������ ������� {b_el} (������: {rand_el})")
    return arr

# ��������� ������ �� 1000 ��������� �����
ans = [random.randint(1, 10) for _ in range(1000000)]
print("������ �� ��������:", ans)

start_time = time.time()  
ans = bb_element(ans)
end_time = time.time()    

print("������ ����� ��������:", ans)
exec_time = end_time - start_time  
print(f"����� ����������: {exec_time} �")
