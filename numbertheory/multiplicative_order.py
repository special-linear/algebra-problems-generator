from problem import Problem
from random import randint
import sympy as sp


def multiplicative_order(n, m):
    k = 1
    nk = n
    while nk != 1:
        k += 1
        nk = nk * n % m
    return k


def number_to_base(n, base):
    if n == 0:
        return [0]
    digits = []
    while n:
        n, digit = divmod(n, base)
        digits.append(int(digit))
    return tuple(digits[::-1])


def fraction_expansion(p, q, base):
    if sp.gcd(q, base) != 1:
        raise ValueError('Denominator and base are not coprime.')
    else:
        d = multiplicative_order(base, q)
        c = (base**d - 1) // q
        pc = p * c
        return ''.join(map(str, number_to_base(pc, base))).zfill(d)


class FractionExpansionPeriod(Problem):
    def __init__(self):
        self.p, self.q = self.gen_fraction_expansion()

    def render(self):
        return 'Найдите период и вычислите восьмеричную запись числа, ' \
               'имеющего в троичной системе счисления запись $0.({})$.'.format(
            fraction_expansion(self.p, self.q, 3)
        )

    @staticmethod
    def gen_fraction_expansion():
        good_number = False
        while not good_number:
            q = 0
            while q % 2 == 0 or q % 3 == 0:
                q = randint(13, 99)
            p = randint(2, q - 1)
            good_number = 4 <= multiplicative_order(3, q) <= 6 and 3 <= multiplicative_order(8, q) <= 6
        return p, q

