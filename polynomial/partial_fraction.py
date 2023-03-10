from problem import Problem
import sympy as sp
from sympy.abc import x
from random import sample, shuffle, choice
import operator
from polynomial.common import poly_to_tex


class PartialFraction(Problem):
    def __init__(self):
        self.numer, self.denom = self.gen_partial_fraction()

    def render(self):
        denom_strs = []
        for deg, root in self.denom:
            denom_str = '{}{}'.format(
                'x' if root == 0 else '(x{}{})'.format('+' if root > 0 else '', root),
                '^{}'.format(deg) if deg > 1 else ''
            )
            denom_strs.append(denom_str)
        return 'Разложить на простейшие дроби\n' \
               '\\[ \\frac{{{}}}{{{}}}. \\]'.format(
            poly_to_tex(self.numer),
            ' \\cdot '.join(denom_strs)
        )
        # return 'Find the partial fraction decomposition of\n' \
        #        '\\[ \\frac{{{}}}{{{}}}. \\]'.format(
        #     poly_to_tex(self.numer),
        #     ' \\cdot '.join(denom_strs)
        # )


    @staticmethod
    def gen_partial_fraction():
        denom_degs = (1, 2, 1)
        denom_roots = list(sample(range(-3, 4), k=len(denom_degs)))
        shuffle(denom_roots)
        expr = 0
        for deg, b in zip(denom_degs, denom_roots):
            for i in range(1, deg + 1):
                expr += choice((1, -1)) * choice((1, 1, 1, 2, 2, 3, 4)) / (x - b)**i
        numer, denom = sp.simplify(expr).as_numer_denom()
        return sp.Poly(numer).all_coeffs(), tuple(zip(denom_degs, map(operator.neg, denom_roots)))
