def is_prime(x):
    if x == 2 or x == 3: return True
    if x == 1 or x % 2 == 0 or x % 3 == 0: return False
    k, step = 5, 2
    while k * k <= x:
        if x % k == 0: return False
        k += step
        step = 6 - step
    return True
