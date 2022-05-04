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


def segment_sieve(ql, qr):
    # [ql, qr)
    # O(sqrt(qr) + (qr - ql)loglog(qr))
    is_prime_sqrt = [True for _ in range(int(qr ** 0.5) + 1)]
    is_prime_sqrt[0] = is_prime_sqrt[1] = False
    is_prime = [True for _ in range(qr - ql)]

    if ql == 0:
        is_prime[0] = is_prime[1] = False
    if ql == 1:
        is_prime[0] = False

    i = 2
    while i * i <= qr:
        if is_prime_sqrt[i]:
            j = 2
            while j * j <= qr:
                is_prime_sqrt[j] = False
                j += i
            for j in range(max((ql + i - 1) // i, 2) * i, qr, i):
                is_prime[j - ql] = False
        i += 1
    primes = [ql + i for i, flag in enumerate(is_prime) if flag]
    return primes
