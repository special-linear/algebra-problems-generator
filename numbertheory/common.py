import operator
from collections import Counter
from functools import reduce

from numbertheory.gaussint import GaussInt


def gen_primes_list(n):
    sieve = [True] * (n//2)
    for i in range(3, int(n**0.5)+1, 2):
        if sieve[i//2]:
            sieve[i*i//2::i] = [False] * ((n-i*i-1)//(2*i)+1)
    return [2] + [2*i+1 for i in range(1, n//2) if sieve[i]]


def primes(n):
    primfac = []
    d = 2
    while d*d <= n:
        while (n % d) == 0:
            primfac.append(d)  # supposing you want multiple factors repeated
            n //= d
        d += 1
    if n > 1:
        primfac.append(n)
    return primfac


primes_list = gen_primes_list(100000)


def euler_phi(n):
    return reduce(operator.mul, (p**(e-1)*(p-1) for p, e in Counter(primes(n)).items()), 1)


# Extended Euclidean algorothm
# Finds x, y such that ax+by=gcd(a,b)
def extgcd(a, b):
    a, b = sorted((a, b))
    s, s_old = 0, 1
    t, t_old = 1, 0
    r, r_old = b, a
    steps = 0
    while r:
        steps += 1
        q = r_old // r
        r_old, r = r, -(q*r-r_old)
        s_old, s = s, -(q*s-s_old)
        t_old, t = t, -(q*t-t_old)
    return r_old, s_old, t_old, steps


units_gaussian = (GaussInt(1, 0), GaussInt(-1, 0), GaussInt(0, 1), GaussInt(0, -1))


def coprime_gaussian(a, b):
    return extgcd(a, b)[0] in units_gaussian


# Solves ax+by=c
# Solution (x, xs, y, ys) means (x+k*xs, y+k*ys), k an integer
def linear_diophantine2(a, b, c):
    d, xp, yp, _ = extgcd(a, b)
    if c % d != 0:
        return None
    else:
        return xp*c//d, yp*c//d
    pass


# Solves ax = b (mod m)
# Solution (x, xs) means x+k*xs, k an integer
def linear_congruence(a, b, m):
    d, x, _, _ = extgcd(a, m)
    if b % d != 0:
        return None
    else:
        return x*b//d, m//d


def pow_mod(a, b, m):
    if b == 0:
        return 1
    elif b < 0:
        a_inv = linear_congruence(a, 1, m)[0]
        return pow_mod(a_inv, -b, m)
    else:
        res = 1
        while b:
            if b & 1:
                res = res * a % m
            a = a*a % m
            b >>= 1
    return res


# checkes whether a is an integer power of b and calculates the logarithm
def is_power(a, b):
    ln = 0
    while a % b == 0:
        a = a//b
        ln += 1
    return bool(a == 1), ln


def powers_tower_eq(pows, s):
    if pows and s != 0:
        if s == 1 and (pows[0] == 1 or (len(pows) > 1 and pows[1] == 0)):
            return True
        else:
            f, ln = is_power(pows[0], s)
            if f:
                if len(pows) > 1:
                    return powers_tower_eq(pows[1:], ln)
                else:
                    return ln == 1
            else:
                return False
    else:
        return s == 0 and pows[0] == 0


def powers_mod(pows, shift, m):
    if len(pows) == 1 or m == 1 or pows[0] == 1:
        return pows[0] % m
    elif m == 2:
        if pows[0] % 2 == 1:
            return 1
        elif powers_tower_eq(pows[1:], -shift):
            return 1
        else:
            return 0
    else:
        d = extgcd(pows[0], m)[0]
        if d == 1:
            pow_res = powers_mod(pows[1:], 0, euler_phi(m))
            return pow_mod(pows[0], pow_res+shift, m)
        else:
            # TODO: how to check whether one actually can have a larger shift? 2^1^1 mod 4
            return (d * powers_mod([pows[0]//d]+pows[1:], shift, m//d) * powers_mod([d]+pows[1:], shift-1, m//d)) % m


# Computes Legendre symbol via quadratic reciprocity law
def legendre_qrl(a, p):
    if a == 1:
        return 1, 1
    if a == 2:
        return 1 if (p % 8 in (1, 7)) else -1, 1
    if a >= p:
        rec = legendre_qrl(a % p, p)
        return rec[0], rec[1]+1
    ap = primes(a)
    if len(ap) > 1:
        acc = 1
        count = 1
        for q, e in Counter(ap).items():
            if e % 2 != 0:
                rec = legendre_qrl(q, p)
                acc *= rec[0]
                count += rec[1]
        return acc, count
    else:
        rec = legendre_qrl(p, a)
        return (1 if (p % 4 == 1) or (a % 4 == 1) else -1)*rec[0], rec[1]+1


# Finds the least quadratic non-residue modulo p
def least_qnr(p):
    if p % 8 not in (1, -1):
        return 2
    else:
        pr = gen_primes_list(p)
        i = 0
        while legendre_qrl(pr[i], p)[0] == 1:
            i += 1
        return pr[i]


# Solves x^2 = a (mod p), p prime, via Tonelli---Shanks algorithm
def tonelli_shanks(a, p):
    steps = 0
    s = p-1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1
    if e == 1:
        return a**((p+1)//4) % p, steps
    else:
        z = least_qnr(p)
        c = z**s % p
        y = a**((s+1)//2) % p
        t = a**s % p
        n = e
        while t != 1:
            steps += 1
            tsq = t
            i = 0
            while tsq != 1:
                tsq = tsq*tsq % p
                i += 1
            b = pow_mod(c, 2**(n-i-1), p)
            c = b*b % p
            y = y*b % p
            t = t*c % p
            n = i
        return y, steps


