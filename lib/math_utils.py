import math
from functools import reduce

def lcm(numbers_list):
    """Return lowest common multiple."""
    def lcm(a, b):
        return (int(a) * int(b)) // math.gcd(int(a), int(b))
    return reduce(lcm, numbers_list, 1)


def pfactors(n):
    step = lambda x: 1 + (x<<2) - ((x>>1)<<1)
    maxq = int(math.floor(math.sqrt(n)))
    d = 1
    q = n % 2 == 0 and 2 or 3
    while q <= maxq and n % q != 0:
        q = step(d)
        d += 1
    return q <= maxq and [q] + pfactors(n//q) or [n]


