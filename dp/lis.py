from bisect import bisect_left, bisect_right

INF = 1 << 60

def lis(n, nums, *, strict=True, return_idx=False):
    n = len(nums)
    search = bisect_right if not strict else bisect_left

    dp = [INF for _ in range(n)]
    idp = [-1 for _ in range(n)]
    for i, num in enumerate(nums):
        pos = search(dp, num)
        dp[pos] = num
        idp[i] = pos

    pos = max(idp)
    lis = [0 for _ in range(pos + 1)]
    for i, num in enumerate(nums[::-1]):
        if idp[~i] == pos:
            lis[pos] = num if not return_idx else n - 1 - i
            pos -= 1
    return lis
