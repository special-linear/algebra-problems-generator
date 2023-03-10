import random

import numpy as np

from linear_algebra.common import *
from numbertheory.gaussint import GaussInt

import itertools

from problem import Problem


class OperatorMatrixPolyToCol(Problem):

    def __init__(self, parameters):
        self.poly_degree, self.col_degree = parameters
        self.operator_rows = self.gen_poly_to_col(*parameters)

    def render(self):
        return 'Оператор $\\varphi$ действует между пространствами ' \
               '$\\mathbb{{R}}[t]_{{\leqslant {}}}$ и $\\mathbb{{R}}^{}$ по правилу\n' \
               '\\[ f \longmapsto \\begin{{pmatrix}} {} \\end{{pmatrix}}. \\]\n' \
               'Найти его матрицу по отношению к каким-нибудь базисам.'.format(
            self.poly_degree, self.col_degree, '\\\\'.join(self.operator_rows)
        )

    @staticmethod
    def gen_poly_to_col(poly_degree, col_degree):
        summands_list = ['f(0)', 'f(1)', 'f(1)', 'f(2)', 'f(-1)', 'f(-2)',
                         "f'(0)", "f'(1)", "f'(-1)", "f''(0)"]
        multiplier_list = ['', '', '2', '3']
        summands_number = 4
        return [''.join(map(''.join,
                            itertools.zip_longest((random.choice(multiplier_list) for _ in range(summands_number - 1)),
                                                  random.sample(summands_list, summands_number),
                                                  (random.choice('+-') for _ in range(summands_number - 1)),
                                                  fillvalue='')))
                for _ in range(col_degree)]


class OperatorMatrixComplexPolyToComplex(Problem):

    def __init__(self, parameters):
        self.poly_degree = parameters[0]
        self.rule = self.gen_complex_poly_to_complex(*parameters)

    def render(self):
        return 'Оператор $\\varphi$ действует между $\mathbb{{R}}$-пространствами ' \
               '$\mathbb{{C}}[t]_{{\leqslant {}}}$ и $\mathbb{{C}}$ по правилу\n' \
               '\\[ f \longmapsto {}. \\]\n' \
               'Найти его матрицу по отношению к каким-нибудь базисам.'.format(
            self.poly_degree, self.rule
        )

    @staticmethod
    def gen_complex_poly_to_complex(poly_degree):
        summands_list = ['f(0)', 'f(1)', 'f(i)', 'f(-1)', 'f(-i)',
                         "f'(0)", "f'(1)", "f'(-1)", "f'(i)", "f'(-i)", "f''(0)"]
        multiplier_list = [*['' for _ in range(3)],
                           'i\cdot ', '2', '2i\cdot ', '(1+i)\cdot ', '(1-i)\cdot ',
                           '(2+i)\cdot ', '(2-i)\cdot ', '(1+2i)\cdot ', '(1-2i)\cdot ']
        modifiers_list = [*['{}' for _ in range(3)],
                          '\operatorname{{Re}}({})', '\operatorname{{Im}}({})', '\overline{{{}}}']
        summands_number = 4
        summands = map(lambda x: x[0].format(x[1]), zip(random.sample(modifiers_list, summands_number),
                                                        random.sample(summands_list, summands_number)))
        return ''.join(map(''.join,
                           itertools.zip_longest((random.choice(multiplier_list) for _ in range(summands_number - 1)),
                                                 summands,
                                                 (random.choice('+-') for _ in range(summands_number - 1)),
                                                 fillvalue='')))


class OperatorMatrixSkewSymmConjByOrth(Problem):
    def __init__(self):
        self.b, self.basis = self.gen_skewsymm_conj_by_orth()

    def render(self):
        return '$V = \\{{ A\in M(3,\mathbb{{R}}) \mid A^\intercal=-A \\}}$ --- векторное пространство над $\mathbb{{R}}$.\n' \
               '\\[ \\varphi \colon A \longmapsto B\cdot A\cdot B^{{-1}}, \quad \\text{{где}} \quad ' \
               'B = \\begin{{pmatrix}} {} \end{{pmatrix}}. \\]\n' \
               'Найти матрицу $\\varphi$ по отношению к базису\n' \
               '\\[ f \colon  {}. \\]'.format(
            ' \\\\ '.join(' & '.join(row) for row in self.b), ',\ '.join(map(matrix_to_tex, self.basis))
        )

    @staticmethod
    def gen_skewsymm_conj_by_orth():
        ssm1 = np.matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]], dtype=int)
        ssm2 = np.matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]], dtype=int)
        ssm3 = np.matrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]], dtype=int)
        ssms = (ssm1, ssm2, ssm3)
        c = gen_glnz_matrix(3, entries_lim=4)
        basis = tuple(sum(c[i, j]*ssms[j] for j in range(3)) for i in range(3))
        b = list(map(lambda r: list(map(str, r)), [[1, 0, 0], [0, 1, 0], [0, 0, 1]]))
        i, j, k = random.sample((0, 1, 2), 3)
        b[i][i] = '\\nicefrac{3}{5}'
        b[i][j] = '\\nicefrac{-4}{5}'
        b[j][i] = '\\nicefrac{4}{5}'
        b[j][j] = '\\nicefrac{3}{5}'
        b[k][k] = random.choice(('1', '-1'))
        return b, basis


class OperatorMatrixTracelessAdjDer(Problem):

    def __init__(self):
        self.b, self.basis = self.gen_traceless_adj_der()

    def render(self):
        return '$V = \\{{ A\in M(2,\mathbb{{R}}) \mid \operatorname{{tr}}(A)=0 \\}}$ --- ' \
               'векторное пространство над $\mathbb{{R}}$ ' \
               '(здесь $\operatorname{{tr}}(A)$ обозначает сумму диагональных элементов).\n' \
               '\\[ \\varphi \colon A \longmapsto AB-BA, \quad \\text{{где}} \quad ' \
               'B = \\begin{{pmatrix}} {} \end{{pmatrix}}. \\]\n' \
               'Найти матрицу $\\varphi$ по отношению к базису\n' \
               '\\[ f \colon  {}. \\]'.format(
            ' \\\\ '.join(' & '.join(row) for row in self.b), ',\ '.join(map(matrix_to_tex, self.basis))
        )

    @staticmethod
    def gen_traceless_adj_der():
        ssm1 = np.matrix([[0, 1], [0, 0]], dtype=int)
        ssm2 = np.matrix([[0, 0], [1, 0]], dtype=int)
        ssm3 = np.matrix([[1, 0], [0, -1]], dtype=int)
        ssms = (ssm1, ssm2, ssm3)
        c = gen_glnz_matrix(3, entries_lim=4)
        basis = tuple(sum(c[i, j] * ssms[j] for j in range(3)) for i in range(3))
        b = [[str(random.choice((-2, -1, 1, 2))) for j in range(2)] for i in range(2)]
        return b, basis


class OperatorMatrixSkewHermConjByUnitary(Problem):
    def __init__(self):
        self.b, self.c = self.gen_skewsymm_conj_by_orth()

    def render(self):
        return '$V = \\{{ A\in M(2,\mathbb{{C}}) \mid A^t=-\overline{{A}} \\}}$' \
               ' --- векторное пространство над $\mathbb{{R}}$.\n' \
               '\\[ \\varphi \colon A \longmapsto B\cdot A\cdot B^{{-1}}, \quad \\text{{где}} \quad ' \
               'B = \\begin{{pmatrix}} {} \end{{pmatrix}}. \\]\n' \
               'Найти матрицу $\\varphi$ по отношению к базису\n' \
               '\\[ f \colon  {}. \\]'.format(
            ' \\\\ '.join(' & '.join(row) for row in self.b),
            ',\ '.join('\\begin{{pmatrix}} {} & {} \\\\ {} & {} \end{{pmatrix}}'.format(
                GaussInt(0, r[0]), GaussInt(r[1], r[2]), GaussInt(-r[1], r[2]), GaussInt(0, r[3])
            ) for r in self.c)
        )

    @staticmethod
    def gen_skewsymm_conj_by_orth():
        c = gen_glnz_matrix(4, entries_lim=5).tolist()
        b = random.choice([[['\\nicefrac{3i}{5}', '\\nicefrac{-4i}{5}'], ['\\nicefrac{4i}{5}', '\\nicefrac{3i}{5}']],
                           [['\\nicefrac{4i}{5}', '\\nicefrac{3i}{5}'], ['\\nicefrac{-3i}{5}', '\\nicefrac{4i}{5}']]])
        return b, c


class OperatorMatrixMatMulComplexConj(Problem):
    # TODO: check that the basis lies in the space
    def __init__(self):
        self.b, self.c = self.gen_mat_mul_complex_conj()

    def render(self):
        return '$V = \\{{ A\in M(2,\mathbb{{C}}) \mid A\cdot\\begin{{psmallmatrix}}2\\\\-1\end{{psmallmatrix}}=0 \\}}$' \
               ' --- векторное пространство над $\mathbb{{R}}$.\n' \
               '\\[ \\varphi \colon A \longmapsto B\cdot \overline{{A}}, \quad \\text{{где}} \quad ' \
               'B = \\begin{{pmatrix}} {} \end{{pmatrix}}. \\]\n' \
               'Найти матрицу $\\varphi$ по отношению к базису $f$:' \
               '\\[ {}. \\]'.format(
            ' \\\\ '.join(' & '.join(map(str, row)) for row in self.b),
            ', '.join('\\begin{{pmatrix}} {} & {} \\\\ {} & {} \end{{pmatrix}}'.format(
                GaussInt(r[0], r[2]), GaussInt(2 * r[0], 2 * r[2]), GaussInt(r[1], r[3]), GaussInt(2 * r[1], 2 * r[3])
            ) for r in self.c)
        )

    @staticmethod
    def gen_mat_mul_complex_conj():
        b = [[random.randint(-4, 4) for _ in range(2)] for __ in range(2)]
        c = gen_glnz_matrix(4, entries_lim=5).tolist()
        return b, c