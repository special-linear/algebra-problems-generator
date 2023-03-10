from random import randint, choice, sample
from math import gcd, prod

from numbertheory.gaussint import GaussInt
from problem import Problem

from numbertheory.common import *
from numbertheory.polynomial import Polynomial


class LinearDiophantine(Problem):

    def __init__(self, parameters=(4, 50, 200, 30, 50), ring='integers', num_variables=2):
        self.ring = ring
        if ring == 'integers':
            if num_variables == 2:
                self.coefficients = self.gen_linear_diophantine2(*parameters)
            elif num_variables == 3:
                self.coefficients = self.gen_linear_diophantine3(*parameters)
        elif ring == 'gaussint':
            self.coefficients = self.gen_linear_diophantine_gaussint(*parameters)
        elif ring == 'polynomial':
            self.coefficients = self.gen_linear_diophantine_polynomial(*parameters)

    def render(self):
        ring_str = {'integers': 'целых чисел $\\mathbb{{Z}}$',
                    'gaussint': 'гауссовых целых $\\mathbb{{Z}}[i]$',
                    'polynomial': 'многочленов $\\mathbb{{Q}}[t]$'}[self.ring]
        variables = 'xyzwuv'
        parentheses = '{}' if self.ring == 'integers' else '({})'
        summands = map(lambda x, y: parentheses.format(x)+y, self.coefficients[:-1], variables)
        return 'Решите линейное уравнение в кольце {}:\n' \
               '\\[ {} = {}. \\]'.format(ring_str, ' + '.join(summands), self.coefficients[-1])
        # return 'Solve the linear Diophantine equation:\n' \
        #        '\\[ {} = {}. \\]'.format(' + '.join(summands), self.coefficients[-1])


    @staticmethod
    def gen_linear_diophantine2(steps, a_lower, a_upper, cp_lower, cp_upper):
        while True:
            a = randint(a_lower, a_upper)
            b = randint(int(0.6 * a), int(0.62 * a))
            ans = extgcd(a, b)
            if ans[0] > 1 and ans[3] == steps:
                cp = randint(cp_lower, cp_upper)
                return a, b, ans[0] * cp

    @staticmethod
    def gen_linear_diophantine3(steps, gcd_lower, limit_lower, limit_upper, dp_lower, dp_upper):
        while True:
            a, b, c = sorted([randint(limit_lower, limit_upper) for _ in range(3)], reverse=True)
            gcdab = extgcd(a, b)
            gcdabc = extgcd(gcdab[0], c)
            if gcdabc[0] >= gcd_lower and gcdabc[0] % 5 != 0 and gcdab[3] >= steps and gcdabc[3] >= steps:
                dp = randint(dp_lower, dp_upper)
                return a, b, c, gcdabc[0] * dp

    @staticmethod
    def gen_linear_diophantine_gaussint(limit_lower, limit_upper, d_limit_lower, d_limit_upper):
        d = GaussInt(randint(d_limit_lower, d_limit_upper), choice((1, -1)) * randint(d_limit_lower, d_limit_upper))
        while True:
            a = GaussInt(randint(limit_lower, limit_upper), choice((1, -1)) * randint(limit_lower, limit_upper))
            b = GaussInt(randint(limit_lower, limit_upper), choice((1, -1)) * randint(limit_lower, limit_upper))
            if coprime_gaussian(a, b):
                c = GaussInt(randint(limit_lower, limit_upper), choice((1, -1)) * randint(limit_lower, limit_upper))
                return a*d, b*d, d*c

    @staticmethod
    def gen_linear_diophantine_polynomial(a_degree, b_degree, d_degree, coeff_limit_lower, coeff_limit_upper):
        d = Polynomial([randint(coeff_limit_lower, coeff_limit_upper) for _ in range(d_degree)])
        while True:
            a = Polynomial([randint(coeff_limit_lower, coeff_limit_upper) for _ in range(a_degree)])
            b = Polynomial([randint(coeff_limit_lower, coeff_limit_upper) for _ in range(b_degree)])
            if extgcd(a, b)[0].deg() == 0:
                c = Polynomial([randint(coeff_limit_lower, coeff_limit_upper) for _ in range(b_degree)])
                return a * d, b * d, d * c


class LinearDiophantineParametric(Problem):
    def __init__(self):
        pass
        self.a1, self.a2, self.b, self.c = self.gen_linear_diophantine_with_powers()

    def render(self):
        return 'Решите при произвольном значении натурального параметра $n$ ' \
               'в целых числах линейное уравнение:\n' \
               '\\[ \left( {}^n + {}^n \\right) x + {} y = {}. \\]'.format(self.a1, self.a2, self.b, self.c)

    @staticmethod
    def gen_linear_diophantine_with_powers():
        while True:
            a1, a2, b = sample(range(11, 50), k=3)
            gcds = list({gcd(a1**n + a2**n, b) for n in range(1000)})
            if len(gcds) == 3 and 1 in gcds:
                c1 = 1
                while c1 in gcds:
                    c1 = randint(3, 49)
                c2 = 1
                while c2 == 1:
                    c2 = choice(gcds)
                c = c1 * c2
                return a1, a2, b, c

