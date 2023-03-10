from problem import Problem
import sympy as sp
from sympy.abc import x
from sympy.polys.domains import ZZ
from random import choices
import itertools as it
from polynomial.common import *


def hensel_lift(f: sp.Poly, f1: sp.Poly, f2: sp.Poly, p: int, m: int):
    f1modp = sp.Poly(f1, modulus=p)
    f2modp = sp.Poly(f2, modulus=p)
    d, r = divmod(sp.Poly(f - f1 * f2, domain=ZZ), p**m)
    if r == 0:
        u, v, h = sp.Poly.gcdex(f1modp, f2modp)
        w, g1 = divmod(sp.Poly(d * v, modulus=p), f1modp)
        g2 = sp.Poly(d * u + w * f2modp, modulus=p)
        pm = p**m
        f1modpm = sp.Poly(f1+pm*g1, modulus=pm*p)
        f2modpm = sp.Poly(f2+pm*g2, modulus=pm*p)
        return sp.Poly(f1modpm, domain=ZZ), sp.Poly(f2modpm, domain=ZZ)
    else:
        return None


class HenselLift(Problem):
    def __init__(self):
        self.f = self.gen_hensel_lift((2, 3), 3, 5)

    def render(self):
        return 'Разложите многочлен\n\\[ f = {} \\]\n' \
               'на неприводимые (над $\\mathbb{{Z}}$) множители при помощи подъема по Гензелю, ' \
               'предварительно разложив его на множители по какому-нибудь простому модулю. ' \
               'В процессе можно пользоваться написанной на занятии программой.'.format(
            poly_to_tex(self.f)
        )

    @staticmethod
    def gen_hensel_lift(degs, p, steps):
        good_f = False
        while not good_f:
            good_factors = False
            while not good_factors:
                coeffs = ([1, *choices(range(-p ** steps, p ** steps + 1), k=deg)] for deg in degs)
                f1, f2 = map(lambda cs: sp.Poly.from_list(cs, x, domain=ZZ), coeffs)
                f1modp, f2modp = map(lambda f: sp.Poly.from_poly(f, x, modulus=p), (f1, f2))
                good_factors = f1modp.is_irreducible and f2modp.is_irreducible and sp.Poly.gcd(f1modp, f2modp) == 1
            f = f1 * f2
            if all(sum(g[1] for g in sp.factor_list(sp.Poly.from_poly(f, x, modulus=q))[1]) >= 4 for q in range(2, p) if sp.isprime(q)):
                for m in it.count(1):
                    f1t, f2t = hensel_lift(f, f1, f2, p, m)
                    f1, f2 = f1t, f2t
                    if f == f1 * f2:
                        if m == steps:
                            good_f = True
                        break
        return f.all_coeffs()
