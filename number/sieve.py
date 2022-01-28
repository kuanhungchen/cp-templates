def sieve(n):
    # O(nlognlogn)
    is_prime = [True for _ in range(n + 1)]
    is_prime[0] = is_prime[1] = False
    i = 2
    while i * i <= n:
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
        i += 1
    primes = [i for i, flag in enumerate(is_prime) if flag]
    return primes, is_prime
