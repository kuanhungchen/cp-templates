def LIS(nums):
    # use bisect_right if asking for longest non-decreasing subsequence
    dp = [INF for _ in range(len(nums) + 1)]
    for num in nums:
        dp[bisect_left(dp, num)] = num
    return bisect_left(dp, INF)
