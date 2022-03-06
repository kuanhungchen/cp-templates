def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return (a * b) // gcd(a, b)

def all_gcd(nums):
    # O(n + log(min(A)))
    return reduce(gcd, nums[1:], nums[0])
