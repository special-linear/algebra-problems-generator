from random import choice, randint

from numbertheory.common import primes_list, legendre_qrl, least_qnr, tonelli_shanks
from problem import Problem


class SquareRootModulo(Problem):
    def __init__(self, parameters=(3, 100, 1000, 7)):
        self.a, self.p = self.gen_tonelli_shanks(*parameters)

    def render(self):
        return 'Решить квадратичное сравнение\n' \
               '\\[ x^2 \equiv {} \\pmod{{{}}}. \\]'.format(self.a, self.p)

    @staticmethod
    def gen_tonelli_shanks(steps, limit_lower, limit_upper, z_lower):
        # pl = list(filter(lambda x: (x >= limit_lower) and (x % 32 == 1), gen_primes_list(limit_upper)))
        pl = list(filter(lambda x: (limit_lower <= x <= limit_upper) and (x % 16 == 1), primes_list))
        while True:
            p = choice(pl)
            if least_qnr(p) >= z_lower:
                a = randint(1, p - 1)
                sqrta = int(a ** 0.5)
                if sqrta * sqrta != a:
                    if legendre_qrl(a, p)[0] == 1:
                        if tonelli_shanks(a, p)[1] >= steps:
                            return a, p