def eratosthenes(n):
    # O(nloglogn)
    is_prime = [True for _ in range(n + 1)]
    is_prime[0] = is_prime[1] = False
    i = 2
    while i * i <= n:
        if is_prime[i]:
            for j in range(2 * i, n + 1, i):
                is_prime[j] = False
        i += 1
    primes = [i for i, flag in enumerate(is_prime) if flag]
    return primes, is_prime


def linear_sieve(n):
    # O(n)
    primes = []
    min_facts = list(range(n + 1))
    for i in range(2, n + 1):
        if min_facts[i] == i:
            primes.append(i)
        for p in primes:
            if p * i > n or p > min_facts[i]:
                break
            min_facts[p * i] = p
    return primes, min_facts

def prime_factors(x, min_facts):
    # O(logn)
    facts = []
    while min_facts[x] != 1:
        facts.append(min_facts[x])
        x //= min_facts[x]
    return facts


def segment_sieve(L, R):
    # [L, R]
    # O((R - L + 1)loglogR + sqrt(R)loglog(sqrt(R)))
    # is_prime[idx] = True means the value `idx` is a prime.
    primes, _ = linear_sieve(int(R ** 0.5))

    is_prime = [True for _ in range(R - L + 1)]
    for p in primes:
        for j in range(max(p * p, ((ql + p - 1) // p) * p), R + 1, p):
            is_prime[j - L] = False
    if L == 1:
        is_prime[0] = False
    return is_prime
