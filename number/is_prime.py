def is_prime(x):
    if x == 2: return True
    if x == 1 or x & 1 == 0: return False
    k = 3
    while k * k <= x:
        if x % k == 0: return False
        k += 2
    return True
