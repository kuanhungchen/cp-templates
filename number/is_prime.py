def is_prime(x):
    # O(sqrt(x))
    if x == 2 or x == 3: return True
    if x == 1 or x % 2 == 0 or x % 3 == 0: return False
    k, step = 5, 2
    while k * k <= x:
        if x % k == 0: return False
        k += step
        step = 6 - step
    return True


def miller_rabin(x):
    # O((log x) ^ 3)
    if x < 2:
        return False

    bases = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for b in bases:
        if x == b:
            return True
        if x % b == 0:
            return False

    r, d = 0, x - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for b in bases:
        b_pow = pow(b, d, x)
        if b_pow == 1 or b_pow == x - 1:
            continue

        for _ in range(r - 1):
            b_pow = pow(b_pow, 2, x)
            if b_pow == x - 1:
                break
        else:
            return False
    return True
