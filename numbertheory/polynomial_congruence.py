from random import choice, sample, randint
from math import gcd, prod
from numbertheory.common import primes

from problem import Problem


class QubicCongruence(Problem):
    def __init__(self):
        self.parameters = self.gen_qubic_congruence()

    def render(self):
        return 'Решить полиномиальное сравнение\n' \
               '\\[ x^3 + {} x + {} \equiv 0 \pmod{{{}}}. \\]'.format(*self.parameters)

    @staticmethod
    def gen_qubic_congruence():
        while True:
            primes = sample([3, 5, 7, 11], 3)
            powers = sample([1, 2, 3], 3)
            m = 1
            for p, d in zip(primes, powers):
                m *= p**d
            for _ in range(100):
                a = randint(m // 6, m // 3)
                b = randint(m // 6, m // 3)
                roots_nums = [len({x for x in range(p**d) if (x**3 + a * x + b) % (p**d) == 0}) for p, d in zip(primes, powers)]
                if list(sorted(roots_nums)) == [1, 1, 3]:
                    return  a, b, m
                # roots = {x for x in range(m) if (pow(x, 3, m) + a * x + b) % m == 0}
                # if len(roots) == 1:
                #     return a, b, m


class PowerCongruence(Problem):
    def __init__(self):
        self.d, self.a, self.p = self.gen_power_congruence()

    def render(self):
        return 'Решить сравнение $x^{{{}}} \\equiv {} \\pmod{{{}}}$.'.format(self.d, self.a, self.p)

    @staticmethod
    def gen_power_congruence():
        primes100 = [97, 101, 103, 107, 109, 113]
        while True:
            p = choice(primes100)
            pm1_factors = primes(p - 1)
            d = randint(21, 75)
            if gcd(d, p - 1) == 1:
                a = 0
                while a <= 10 or a >= p - 10:
                    a = randint(3, 19) * prod(sample(pm1_factors, k=2)) % p
                return d, a, p
