def prime_factors(x):
    # return all prime factors of x, O(sqrt(x))
    facts = []
    k = 2
    while k * k <= x:
        while x % k == 0:
            facts.append(k)
            x //= k
        k += 1
    if x > 1:
        facts.append(x)
    return facts
