from problem import Problem
import sympy as sp
from sympy.abc import x
import itertools as it
import more_itertools as mit
from random import randint, sample, choices, choice, shuffle
import sys
from polynomial.common import *


small_primes = [2, 3, 5, 7, 11]


def eisenstein(f):
    coeffs = f.all_coeffs()
    for p in small_primes:
        if coeffs[0] % p != 0 and all(c % p == 0 for c in coeffs[1:]) and coeffs[-1] % (p*p) != 0:
            return p
    return False


def eisenstein_shifted(f):
    for a in sorted(range(-9, 10), key=abs):
        if a != 0:
            if eisenstein(sp.compose(f, x-a)):
                return a
    return False


def eisenstein_reversed(f):
    fi = sp.Poly.from_list(reversed(f.all_coeffs()), x)
    return eisenstein(fi)


def dumas_p(f, p):
    coeffs = list(reversed(f.all_coeffs()))
    n = len(coeffs)
    points = {i: sp.multiplicity(p, a) for i, a in enumerate(coeffs) if a != 0}
    print(points)
    newton_points = [(0, points[0])]
    k = 0
    while k < len(points) - 1:
        a = points[k]
        i = 0
        flag = False
        while n - i > k + 1 and not flag:
            i -= 1
            if n + i in points:
                b = points[n + i]
                if isinstance(b, int):
                    alpha = (b - a) / (n - k + i)
                    beta = a - alpha * k
                    flag = all(
                        points[j] == sp.oo or alpha * j + beta <= points[j] for j in range(k + 1, n + i) if j in points)
        k = n + i
        newton_points.append((k, points[k]))
    print(newton_points)
    newton_diagram = set(newton_points)
    for p1, p2 in mit.pairwise(newton_points):
        i1, a1 = p1
        i2, a2 = p2
        for j in range(i1 + 1, i2):
            pj_div, pj_mod = divmod((j - i1) * (a2-a1), (i2 - i1))
            if pj_mod == 0:
                pj = pj_div + a1
                newton_diagram.add((j, pj))
    print(newton_diagram)
    return len(newton_diagram) == 2


def dumas(f):
    for p in small_primes:
        if dumas_p(f, p):
            return p
    return False


def dumas_shifted(f):
    for a in it.chain.from_iterable([i, -i] for i in range(1, 10)):
        if a != 0:
            if dumas(sp.compose(f, x-a)):
                return a
    return False


def perron_strict(f):
    coeffs = f.all_coeffs()
    return bool(coeffs[0] == 1 and coeffs[-1] != 0 and abs(coeffs[1]) > 1 + sum(map(abs, coeffs[2:])))
    # and (f.eval(1) == 0 or f.eval(-1) == 0))


def perron_nonstrict(f):
    coeffs = f.all_coeffs()
    return bool(coeffs[0] == 1 and coeffs[-1] != 0 and abs(coeffs[1]) == 1 + sum(map(abs, coeffs[2:])) and f.eval(
        1) != 0 and f.eval(-1) != 0)


def brauer(f):
    coeffs = f.all_coeffs()
    return len(coeffs) >= 3 and coeffs[0] == 1 and coeffs[-1] < 0 and all(
        a1 <= a2 for a1, a2 in mit.pairwise(coeffs[1:]))


def osada(f):
    coeffs = f.all_coeffs()
    return sp.isprime(abs(coeffs[-1])) and abs(coeffs[-1]) > sum(map(abs, coeffs[:-1]))


def osada_shifted(f):
    for a in it.chain.from_iterable([i, -i] for i in range(1, 10)):
        if a != 0:
            if osada(sp.compose(f, x-a)):
                return a
    return False


def mod_p(f, p):
    fp = sp.Poly.from_poly(f, modulus=p)
    return f.degree() == fp.degree() and fp.is_irreducible


def mod(f):
    # for p in [2, 3, 5]:
    for p in small_primes:
        if mod_p(f, p):
            return p
    return False


def random_primitive_irreducible(deg, coeffs_lim, lc_coeff_lim):
    while True:
        f = random_poly(deg, -coeffs_lim, coeffs_lim, lc_coeff_lim)
        if f.is_primitive and f.is_irreducible:
            return f


def random_poly_for_brauer_test(deg, coeffs_lim, lc_coeff_lim):
    while True:
        f = random_poly(deg, -coeffs_lim, -1, 1)
        if f.is_primitive and f.is_irreducible:
            return f


class IrreducibilityTests(Problem):
    def __init__(self):
        self.polynomials = []

    def render(self):
        return 'Для каждого многочлена $f$ из следующего списка доказать его неприводимость в $\\mathbb{{Z}}[x]$.\n' \
               '\\begin{{enumerate}}\n{}\n\\end{{enumerate}}'.format(
            '\n'.join('\\item $f = {}$'.format(poly_to_tex(f)) for f in self.polynomials)
        )

    @staticmethod
    def gen_batch(num):
        deg = 5
        coeffs_lim = 9
        lc_coeff_lim = 9
        # tests are either functions or pairs of functions (easy_check, hard_check)
        tests = {
            'eisenstein': lambda g: eisenstein_shifted(g) and not eisenstein(g),
            'dumas': (dumas, lambda g: dumas(g) and not eisenstein(g) and not eisenstein_reversed(g)),
            'perron_strict': perron_strict,
            'perron_nonstrict': perron_nonstrict,
            'brauer': brauer,
            'mod2': lambda g: mod_p(g, 2),
            'mod3': lambda g: mod_p(g, 3),
            'mod5': lambda g: mod_p(g, 5)
        }
        good_irreducibles = {test_name: set() for test_name in
                             ['eisenstein', 'dumas', 'perron_strict', 'perron_nonstrict', 'brauer', 'mod2', 'mod3']}
        polynomial_generators = (random_primitive_irreducible, random_poly_for_brauer_test)
        while any(len(problems) < num for problems in good_irreducibles.values()):
            f = choice(polynomial_generators)(deg, coeffs_lim, lc_coeff_lim)
            if not osada(f):
                positive_tests_results = []
                for test_name, test in tests.items():
                    if isinstance(test, tuple):
                        test = test[0]
                    test_result = test(f)
                    if test_result:
                        positive_tests_results.append(test_name)
                if len(positive_tests_results) == 1:
                    test_name = positive_tests_results[0]
                    if test_name in good_irreducibles and len(good_irreducibles[test_name]) < 100:
                        test = tests[test_name]
                        if isinstance(test, tuple):
                            hard_check = test[1](f)
                        else:
                            hard_check = True
                        if hard_check:
                            good_irreducibles[test_name].add(tuple(f.all_coeffs()))
                    sys.stdout.write('\r' + str({k: len(v) for k, v in good_irreducibles.items()}))
                    sys.stdout.flush()
        problems = [IrreducibilityTests() for _ in range(num)]
        for polys in good_irreducibles.values():
            distinct_polys = sample(polys, k=num)
            for pr, f in zip(problems, distinct_polys):
                pr.polynomials.append(f)
        for pr in problems:
            shuffle(pr.polynomials)
        return problems
