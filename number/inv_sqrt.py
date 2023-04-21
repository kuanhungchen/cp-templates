from struct import pack, unpack

def inverse_sqrt(x):
    """Return 1 / sqrt(x).
    https://en.wikipedia.org/wiki/Fast_inverse_square_root
    """
    ITERATION = 3
    MAGIC = 0x5F3759DF
    THREEHALFS = 1.5

    x2 = x * 0.5
    y = x

    y = pack('f', y)
    y = unpack('i', y)[0]
    z = MAGIC - (y >> 1)
    z = pack('i', z)
    z = unpack('f', z)[0]

    for _ in range(ITERATION):
        z = z * (THREEHALFS - (x2 * z * z))
    return z
