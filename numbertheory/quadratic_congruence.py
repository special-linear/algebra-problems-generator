from random import choice, randint

from numbertheory.common import primes_list, legendre_qrl
from problem import Problem


class QuadraticCongruence(Problem):

    def __init__(self, parameters=(5, 100, 3000)):
        self.a, self.b, self.c, self.p = self.gen_quadratic_congruence(*parameters)

    def render(self):
        return 'Определить, разрешимо ли квадратичное сравнение\n' \
               '\\[ {}x^2 + {}x + {} \equiv 0 \\pmod{{{}}}. \\]'.format(self.a, self.b, self.c, self.p)

    @staticmethod
    def gen_legendre_qrl(steps, limit_lower, limit_upper):
        # pl = list(filter(lambda x: x >= limit_lower, gen_primes_list(limit_upper)))
        pl = list(filter(lambda x: limit_lower <= x <= limit_upper, primes_list))
        while True:
            p = choice(pl)
            a = randint(limit_lower, p - 1)
            sqrta = int(a ** 0.5)
            if sqrta * sqrta != a:
                if legendre_qrl(a, p)[1] == steps:
                    return a, p

    @staticmethod
    def gen_quadratic_congruence(steps, limit_lower, limit_upper):
        while True:
            disc, p = QuadraticCongruence.gen_legendre_qrl(steps, limit_lower, limit_upper)
            for _ in range(25):
                a = randint(limit_lower, p - 1)
                b = randint(limit_lower, p - 1)
                c = randint(limit_lower, p - 1)
                if (abs(a-b)) > 500 and abs(a-c) > 500 and abs(b-c) > 500 and (b*b - 4*a*c) % p == disc:
                    return a, b, c, p

