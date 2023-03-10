from problem import Problem
from random import randint, choice
import sympy as sp
from linear_algebra.common import gen_glnz_matrix2, vector2tex


class DualBasisPolynomials(Problem):
    def __init__(self):
        self.a, self.b, self.p1, self.p2 = self.gen_dual_basis()

    def render(self):
        return 'Рассмотрим пространство $V=\\mathbb{{R}}[t]_{{\\leqslant 3}}$ вещественных многочленов степени ' \
               'не выше $3$. Найдите в $V$ базис, ' \
               'двойственный базису $V^*$, составленному из функционалов\n' \
               '\\[ e_1^* = \\int_{{{}}}^{{{}}}, \\quad e_2^* = \\operatorname{{ev}}_{{{}}}, \\quad ' \
               'e_3^* = \\operatorname{{ev}}_{{{}}}\\circ\\frac{{\\mathrm{{d}}}}{{\\mathrm{{d}}t}}, \\quad ' \
               'e_4^* = \\operatorname{{ev}}_0. \\]'.format(
            self.a, self.b, self.p1, self.p2
        )

    @staticmethod
    def gen_dual_basis():
        flag = False
        while not flag:
            b = randint(1, 2)
            a = randint(-1, b - 1)
            p1 = choice((1, -1)) * randint(1, 3)
            p2 = choice((1, -1)) * randint(1, 3)
            m = sp.Matrix([[6 * (b**2 - a**2), 4 * (b**3 - a**3), 3 * (b**4 - a**4)],
                           [p1, p1**2, p1**3],
                           [1, 2 * p2, 3 * p2**2]])
            flag = m.det() != 0
        return a, b, p1, p2


class DualBasisColumns(Problem):
    def __init__(self):
        self.dim, self.basis = self.gen_dual_basis()

    def render(self):
        return 'Рассмотрим следующий базис пространства столбцов $\\mathbb{{R}}^{{{dim}}}$:\n\\[ {basis}. \\]\n' \
               'Найдите двойственный базис, отождествив $(\\mathbb{{R}}^{{{dim}}})^*$ с пространством строк.'.format(
            dim=self.dim, basis=',\quad '.join(map(vector2tex, self.basis))
        )
        # return 'Consider the following basis of the column space $\\mathbb{{R}}^{{{dim}}}$:\n\\[ {basis}. \\]\n' \
        #        'Find its dual basis, identifying $(\\mathbb{{R}}^{{{dim}}})^*$ and the row space.'.format(
        #     dim=self.dim, basis=',\quad '.join(map(vector2tex, self.basis))
        # )

    @staticmethod
    def gen_dual_basis():
        dim = 4
        a = gen_glnz_matrix2(dim, entries_lim=4)
        basis = tuple(map(tuple, sp.Matrix.tolist(a)))
        return dim, basis

