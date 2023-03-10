from random import randint

from numbertheory.common import extgcd
from problem import Problem
import sympy as sp


class LinearCongruence(Problem):
    def __init__(self, parameters=(10, 5, 100, 1000, 10, 100)):
        self.a, self.b, self.m = self.gen_linear_congruence(*parameters)

    def render(self):
        return 'Решить уравнение в кольце вычетов:\n\\[ {}x \equiv {} \\pmod{{{}}}. \\]'.format(self.a, self.b, self.m)
        # return 'Solve the equation in the residue ring:\n\\[ {}x \equiv {} \\pmod{{{}}}. \\]'.format(self.a, self.b, self.m)

    @staticmethod
    def gen_linear_congruence(steps, gcd_lower, limit_lower, limit_upper, bp_lower, bp_upper):
        while True:
            a, m = sorted([randint(limit_lower, limit_upper) for _ in range(2)])
            ans = extgcd(a, m)
            if ans[0] >= gcd_lower and ans[0] % 5 != 0 and ans[3] == steps:
                bp = ans[0] * randint(bp_lower, bp_upper) % m
                if bp != 0 and bp % a != 0:
                    return a, bp, m


class LinearCongruenceTheory(Problem):
    def __init__(self):
        self.a1, self.m1, self.b2, self.m2, self.a3, self.b3 = self.gen_linear_congruence_theory()

    def render(self):
        return 'Ответьте на следующие вопросы с кратким обоснованием. \\begin{{enumerate}} ' \
               '\\item Сколько существует таких $b=1,\\ldots,{}$, что сравнение ${}x\\equiv b\\pmod{{{}}}$ разрешимо? ' \
               '\\item Сколько существует таких $a=1,\\ldots,{}$, что сравнение $ax\\equiv{}\\pmod{{{}}}$ разрешимо? ' \
               '\\item Сколько существует таких $m=2,\\ldots,30$, что сравнение ${}x\\equiv{}\\pmod{{m}}$ разрешимо?' \
               '\\end{{enumerate}}'.format(
            self.m1 - 1, self.a1, self.m1, self.m2 - 1, self.b2, self.m2, self.a3, self.b3
        )

    @staticmethod
    def gen_linear_congruence_theory():
        a1, m1 = 0, 0
        d = sp.gcd(a1, m1)
        while not a1 and not m1 or not (m1 // 3 <= len([b for b in range(1, m1) if b % d == 0]) <= 2 * m1 // 3):
            m1 = randint(10, 30)
            a1 = randint(5, m1 - 1)
            d = sp.gcd(a1, m1)
        b2, m2 = 0, 0
        while not b2 and not m2 or not (m1 // 3 <= len([a for a in range(1, m2) if b2 % sp.gcd(a, m2) == 0]) <= 2 * m1 // 3):
            m2 = randint(10, 30)
            b2 = randint(5, m2 - 1)
        a3, b3 = 0, 0
        while not a3 and not b3 or not (12 <= len([m for m in range(2, 30) if b3 % sp.gcd(a3, m) == 0]) <= 17):
            a3 = randint(10, 29)
            b3 = randint(5, 25)
        return a1, m1, b2, m2, a3, b3
