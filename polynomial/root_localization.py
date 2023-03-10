from problem import Problem

import more_itertools as mit
import cmath
import math
from collections import Counter
from random import sample, choice
from polynomial.common import *


def dominate_on_circle(f1, f2, center, radius, subdivide):
    diff = 1
    min_diff = min(abs(f1.eval(z)) - abs(f2.eval(z)) for z in
                   map(lambda i: radius * cmath.exp(2 * cmath.pi * i / subdivide * 1j) + center, range(subdivide)))
    return min_diff


class RootLocalizationSturm_old(Problem):
    def __init__(self):
        self.f = self.gen_root_localization()

    def render(self):
        return 'Дан многочлен\n\\[ f = {}. \\]\nВычислить количество его вещественных корней на каждом отрезке ' \
               'вида $[k,k+1]$, $k\\in\\mathbb{{Z}}$, где таковые имеются.'.format(
            poly_to_tex(self.f)
        )

    @staticmethod
    def gen_root_localization():
        poly_is_good = False
        while not poly_is_good:
            f = random_poly(5, -7, 7, 3)
            real_roots = f.real_roots()
            if len(real_roots) == f.degree() and sp.gcd(f, f.diff()).degree() == 0 and all(
                    g[0].degree() > 1 for g in f.factor_list()[1]):
                roots_unit_intervals = Counter(map(math.floor, real_roots))
                poly_is_good = all(a[1] > 1 for a in roots_unit_intervals.most_common(2))
        return tuple(f.all_coeffs())


class RootLocalizationSturm(Problem):
    def __init__(self):
        self.f = self.gen_root_localization()

    def render(self):
        return 'Дан многочлен\n\\[ f = {}. \\]\nВычислить количество его вещественных корней на каждом отрезке ' \
               'вида $[k,k+1]$, $k\\in\\mathbb{{Z}}$, где таковые имеются.'.format(
            poly_to_tex(self.f)
        )

    @staticmethod
    def gen_root_localization():
        n = 5
        poly_is_good = False
        while not poly_is_good:
            coeffs = [randint(1, 3)] + [0] * (n - 1) + [randint(-7, 7)]
            for i in sample(range(1, n), 2):
                coeffs[i] = randint(1, 7) * choice((1, -1))
            f = sp.Poly.from_list(coeffs, x, domain='QQ')
            f0, f1 = f, f.diff()
            if sp.gcd(f0, f1).degree() == 0 and len(f.real_roots()) >= 3 and all(g[0].degree() > 1 for g in f.factor_list()[1]):
                sturm_seq = [f0, f1]
                while f1.degree() > 0:
                    f0, f1 = f1, -f0.rem(f1)
                    f1c = f1.content()
                    if f1c:
                        f1 = f1.mul_ground(1/f1.content())
                    sturm_seq.append(f1)
                if len(sturm_seq) == 6:
                    all_sturm_coeffs = set()
                    for g in sturm_seq:
                        all_sturm_coeffs.update(g.coeffs())
                    poly_is_good = all(abs(c) < 100 for c in all_sturm_coeffs)
        return tuple(f.all_coeffs())


class RootLocalizationRouche(Problem):
    def __init__(self):
        self.f = self.gen_root_localization()

    def render(self):
        return 'Дан многочлен\n\\[ f = {}. \\]\nВычислить количество его комплексных корней, имеющих модуль ' \
               'между $k$ и $k+1$, для всех $k\\in\\mathbb{{Z}}$, при которых такие существуют.'.format(
            poly_to_tex(self.f)
        )

    @staticmethod
    def gen_root_localization():
        poly_is_good = False
        while not poly_is_good:
            f = random_poly(4, -5, 5, 5)
            roots = f.nroots(n=5)
            if all(1 < abs(r) < 2 for r in roots) and all(abs(complex(r).imag) > 0.1 for r in roots):
                poly_is_good = True
        return tuple(f.all_coeffs())


class RootLocalizationHalfPlane(Problem):
    def __init__(self):
        self.f = self.gen_root_localization()

    def render(self):
        return 'Дан многочлен\n\\[ f = {}. \\]\n Вычислить количество его комплексных корней в каждой ' \
               'вертикальной полосе $k<\\operatorname{{Re}}(z)<k+1$, $k\\in\\mathbb{{Z}}$.'.format(
            complex_poly_to_tex(self.f)
        )

    @staticmethod
    def gen_root_localization():
        while True:
            f = random_poly(4, -2, 2, 1) + sp.I * random_poly(4, -2, 2, 1)
            roots = f.nroots(n=5)
            roots_real, roots_imag = map(list, mit.unzip(r.as_real_imag() for r in roots))
            if all(rr - sp.floor(rr) > 0.1 and sp.ceiling(rr) - rr > 0.1 for rr in roots_real) and all(ri - sp.floor(ri) > 0.1 and sp.ceiling(ri) - ri > 0.1 for ri in roots_imag):
                roots_by_stripes = mit.bucket(roots_real, key=lambda rr: int(sp.floor(rr)))
                stripes = list(roots_by_stripes)
                if len(stripes) == 2:
                    s1, s2 = stripes
                    if abs(s1 - s2) > 1 and mit.ilen(roots_by_stripes[s1]) != mit.ilen(roots_by_stripes[s2]):
                        # poly_is_good = True
                        return f.all_coeffs()


class RootLocalizationQuadrants(Problem):
    def __init__(self):
        self.f = self.gen_root_localization()

    def render(self):
        return 'Дан многочлен\n\\[ f = {}. \\]\nВычислить количество его комплексных корней ' \
               'в каждой координатной четверти.'.format(complex_poly_to_tex(self.f))

    @staticmethod
    def gen_root_localization():
        while True:
            f = random_poly(4, -2, 2, 1) + choice((1, -1)) * sp.I * random_poly(3, -2, 2, 2)
            roots = f.nroots(n=5)
            roots_real_imag = [r.as_real_imag() for r in roots]
            roots_real, roots_imag = mit.unzip(roots_real_imag)
            if all(abs(rr) > 0.1 for rr in roots_real) and all(abs(ri) > 0.1 for ri in roots_imag):
                roots_by_quadrants = mit.bucket(roots_real_imag, lambda r: (sp.sign(r[0]), sp.sign(r[1])))
                quadrants = list(roots_by_quadrants)
                if len(quadrants) == 3:
                    return f.all_coeffs()

