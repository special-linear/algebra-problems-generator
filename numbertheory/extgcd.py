from random import randint, choice, choices, sample
from math import prod, gcd
import itertools as it

from numbertheory.common import *
from numbertheory.gaussint import GaussInt
from numbertheory.polynomial import Polynomial
from problem import Problem
from pool_problem import FromPoolProblem


class ExtGCD(Problem):
    def __init__(self, parameters=(10, 100, 5000), ring='integers'):
        self.ring = ring
        if ring == 'integers':
            self.a, self.b = self.gen_extgcd(*parameters)
        elif ring == 'gaussint':
            self.a, self.b = self.gen_extgcd_gaussint(*parameters)
        elif ring == 'polynomial':
            self.a, self.b = self.gen_extgcd_polynomial(*parameters)

    def render(self):
        ring_str = {'integers': 'целых чисел $\\mathbb{{Z}}$',
                    'gaussint': 'гауссовых целых $\\mathbb{{Z}}[i]$',
                    'polynomial': 'многочленов $(\\mathbb{{Z}}/5\\mathbb{{Z}})[t]$'}[self.ring]
        return 'Вычислить наибольший общий делитель и его линейное представление в кольце {}:\n' \
               '\\[ \gcd( {}, {} ). \\]'.format(ring_str, self.a, self.b)
        # return 'Calculate the greatest common divisor and find the Bezout coefficients:\n' \
        #        '\\[ \gcd( {}, {} ). \\]'.format(self.a, self.b)

    @staticmethod
    def gen_extgcd(steps, limit_lower, limit_upper):
        while True:
            a = randint(limit_lower, limit_upper)
            b = randint(int(0.6 * a), int(0.62 * a))
            if extgcd(a, b)[3] >= steps:
                return a, b

    @staticmethod
    def gen_extgcd_gaussint(steps,limit_lower, limit_upper, d_limit_lower, d_limit_upper):
        while True:
            d = GaussInt(randint(d_limit_lower, d_limit_upper), choice((1, -1))*randint(d_limit_lower, d_limit_upper))
            a = d * GaussInt(randint(limit_lower, limit_upper), choice((1, -1))*randint(limit_lower, limit_upper))
            b = d * GaussInt(randint(limit_lower, limit_upper), choice((1, -1))*randint(limit_lower, limit_upper))
            if d.r != 0 and d.i != 0 and a.r != 0 and a.i != 0 and b.r != 0 and b.i != 0 and extgcd(a, b)[3] >= steps:
                return a, b

    @staticmethod
    def gen_extgcd_polynomial(steps,a_degree, b_degree, d_degree, coeff_limit_lower, coeff_limit_upper):
        while True:
            d = Polynomial([randint(coeff_limit_lower, coeff_limit_upper) for _ in range(d_degree)])
            a = d * Polynomial([randint(coeff_limit_lower, coeff_limit_upper) for _ in range(a_degree)])
            b = d * Polynomial([randint(coeff_limit_lower, coeff_limit_upper) for _ in range(b_degree)])
            if extgcd(a, b)[3] >= steps:
                return a, b


class GCDPowers(Problem):
    def __init__(self):
        self.b, self.a1, self.a2, self.c1, self.c2, self.d1, self.d2 = self.gen_gcd_powers()

    def render(self):
        return 'Вычислить $\\gcd\\left( {}\\cdot{}^{{{}}}{}{}, {}\\cdot{}^{{{}}}{}{} \\right)$.'.format(
            self.a1, self.b, self.c1, '+' if self.d1 > 0 else '', self.d1,
            self.a2, self.b, self.c2, '+' if self.d2 > 0 else '', self.d2
        )

    @staticmethod
    def gen_gcd_powers():
        x, y = 0, 0
        steps = 0
        good_coeffs = False
        while not (3 <= gcd(x, y) <= 9) or not good_coeffs:
            steps += 1
            # a1 * b^c1 + d1
            a1, a2 = (randint(2, 9) for _ in range(2))
            b = prod(sample((3, 5, 7, 11), k=2))
            c1, c2 = (randint(20, 40) for _ in range(2))
            c1 += c2
            d1, d2 = (choice((1, -1)) * randint(2, 9) for _ in range(2))
            good_coeffs = gcd(a1, a2, d1, d2) == 1
            x = a1 * b ** c1 + d1
            y = a2 * b ** c2 + d2
        return b, a1, a2, c1, c2, d1, d2


class GCDPolynomialExpressions(Problem):
    def __init__(self):
        self.f, self.g = self.gen_gcd_polynomial_expressions()

    def render(self):
        return 'Для каждого целого $n$ вычислить $\\gcd\\left( {}, {} \\right)$.'.format(self.f, self.g)

    @staticmethod
    def gen_gcd_polynomial_expressions():
        good_polys = False
        steps = 0
        lc_coeffs = list(range(2, 9))
        coeffs = list(it.chain(range(-9, 0), range(1, 9)))
        while not good_polys:
            steps += 1
            f_lc, g_lc = sample(lc_coeffs, k=2)
            f_coeffs = [f_lc] + choices(coeffs, k=3)
            g_coeffs = [g_lc] + choices(coeffs, k=2)
            f = Polynomial(coefficients=f_coeffs, variable='n')
            g = Polynomial(coefficients=g_coeffs, variable='n')
            if gcd(*f_coeffs) == 1 and gcd(*g_coeffs) == 1:
                gcd_vals_short = {gcd(f(a), g(a)) for a in range(30)}
                if len(gcd_vals_short) == 3 and 1 not in gcd_vals_short:
                    good_polys = len({gcd(f(a), g(a)) for a in range(10000)}) == 3
        return f, g


class ExtGCDTheory(FromPoolProblem):
    pool = [
        'Единственно ли линейное представление наибольшего общего делителя?',
        'В каких случаях оба коэффициента линейного представления НОД можно выбрать положительными?',
        'Что о паре чисел $a,b\\in\\mathbb{Z}$ говорит наибольший элемент множества \\[\\{ax+by\\mid x,y\\in\\mathbb{Z}\\}\\cap\\mathbb{Z}_{<0}?\\]',
        'Что о тройке чисел $a,b,c\\in\\mathbb{Z}$ говорит наименьший элемент множества \\[\\{ax+by+cz\\mid x,y,z\\in\\mathbb{Z}\\}\\cap\\mathbb{N}?\\]',
    ]
    multiplicity = 5

    def render(self):
        return 'Ответьте на следующие вопросы с кратким обоснованием. {}'.format(super().render())
