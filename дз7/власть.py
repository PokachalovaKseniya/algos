def max_subarray(nums, left, right):
    if left == right:
        return nums[left]
    
    mid = (left + right) // 2
    
    left_max = max_subarray(nums, left, mid)
    right_max = max_subarray(nums, mid + 1, right)
    cross_max = max_crossing_subarray(nums, left, mid, right)
    
    return max(left_max, right_max, cross_max)

def max_crossing_subarray(nums, left, mid, right):
    left_sum = -float('inf')
    current_sum = 0
    for i in range(mid, left - 1, -1):
        current_sum += nums[i]
        if current_sum > left_sum:
            left_sum = current_sum
    
    right_sum = -float('inf')
    current_sum = 0
    for i in range(mid + 1, right + 1):
        current_sum += nums[i]
        if current_sum > right_sum:
            right_sum = current_sum
    
    return left_sum + right_sum

n = int(input())
nums = list(map(int, input().split()))
print(max_subarray(nums, 0, n - 1))