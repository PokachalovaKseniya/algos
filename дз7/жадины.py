def can_partition(nums):
    total_sum = sum(nums)
    if total_sum % 2 != 0:
        return False
    half_sum = total_sum // 2
    dp = [False] * (half_sum + 1)
    dp[0] = True 
    
    for num in nums:
        for j in range(half_sum, num - 1, -1):
            if dp[j - num]:
                dp[j] = True
    return dp[half_sum]

n = int(input())
nums = list(map(int, input().split()))
print(can_partition(nums))