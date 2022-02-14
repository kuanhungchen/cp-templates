def divisors(x):
    # return all divisors of x
    divs1, divs2 = [], []
    k = 1
    while k * k <= x:
        if x % k == 0:
            divs1.append(k)
            if k * k != x:
                divs2.append(x // k)
        k += 1
    divs2.reverse()
    return divs1 + divs2
