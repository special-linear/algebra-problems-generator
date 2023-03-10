from problem import Problem
from list_problem import FromListProblem
from random import choice
from polynomial.common import *


class TaylorPolynomial(Problem):
    def __init__(self):
        self.f_coeffs, self.a, self.b = self.gen_taylor_polynomial()

    def render(self):
        return 'Дан многочлен\n\\[ f = {}. \\]\nИспользуя схему Горнера, вычислить коэффициенты $f({}x{:+})$.'.format(
            poly_to_tex(self.f_coeffs, 'x'), self.a, self.b
        )

    @staticmethod
    def gen_taylor_polynomial():
        good_poly = False
        while not good_poly:
            f = random_poly(4, -9, 9, 1)
            a = choice((1, -1)) * randint(2, 4)
            b = choice((1, -1)) * randint(2, 5)
            g = sp.compose(f, a * x + b)
            good_poly = all(-100 < c < 100 for c in g.all_coeffs())
        return f.all_coeffs(), a, b


class PolynomialReduction(Problem):
    def __init__(self):
        self.f_deg1, self.f_deg2, self.f_coeff2, self.g_coeffs = self.gen_polynomial_reduction()

    def render(self):
        return 'Вычислить остаток от деления многочлена $f = x^{{{}}}+{}x^{{{}}}$ на $g = {}$, считая, что $f$ и $g$ ' \
               'являются многочленами над $\\mathbb{{Z}}/5\\mathbb{{Z}}$.'.format(
            self.f_deg1, self.f_coeff2, self.f_deg2, poly_to_tex(self.g_coeffs, 'x')
        )

    @staticmethod
    def gen_polynomial_reduction():
        xx = sp.Poly(x, modulus=5)
        rem_is_good = False
        while not rem_is_good:
            f_deg1 = randint(100, 200)
            f_deg2 = randint(50, 90)
            f_coeff2 = randint(2, 4)
            f = xx**f_deg1 + (xx**f_deg2).mul_ground(f_coeff2)
            g_coeffs = (1, 0, randint(2, 3), 0, randint(2, 3))
            g = sp.Poly.from_list(g_coeffs, x, modulus=5)
            r = sp.rem(f, g)
            if r.nth(0) == 0 and len(r.coeffs()) > 2:
                rem_is_good = True
        return f_deg1, f_deg2, f_coeff2, tuple(g.all_coeffs())


class DivisibilityParametric(FromListProblem):
    problems = [
        'При каких $m,n,k$ многочлен $x^m-x^n+x^k$ делится на $x^2-x+1$?',
        'При каких $m,n,k$ многочлен $x^m+x^n+x^k$ делится на $x^2+x+1$?',
        'При каких $m$ многочлен $(x+1)^m-x^m+1$ делится на $x^2+x+1$?',
        'При каких $m$ многочлен $(x-1)^m+x^m+1$ делится на $x^2-x+1$?',
        'При каких $m$ многочлен $(x+1)^m+x^m+1$ делится на $x^2+x+1$?',
    ]
    # problems = [
    #     r'При каких $m\in\mathbb{N}$ многочлен $(x+1)^m-x^m-1$ делится на $(x^2+x+1)^2$?',
    #     r'При каких $m\in\mathbb{N}$ многочлен $(x-1)^m+x^m+1$ делится на $(x^2-x+1)^2$?',
    #     r'При каких $m\in\mathbb{N}$ многочлен $(x+1)^m+x^m+1$ делится на $(x^2+x+1)^2$?',
    # ]