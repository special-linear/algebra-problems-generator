from problem import Problem
from linear_algebra.common import *
import sympy as sp
from random import randint

class LinearMatrixEquation(Problem):
    def __init__(self):
        self.a, self.b = self.gen_matrix_equation()

    def render(self):
        return 'Найти все матрицы $X$, удовлетворяющие уравнению\n' \
               '\\[ {} \\cdot X = {}. \\]'.format(
            matrix_to_tex(self.a), matrix_to_tex(self.b)
        )
        # return 'Find all matrices $X$ such that\n' \
        #        '\\[ {} \\cdot X = {}. \\]'.format(
        #     matrix_to_tex(self.a), matrix_to_tex(self.b)
        # )


    @staticmethod
    def gen_matrix_equation():
        # A is an mxn matrix, X is an nxk matrix, B is an mxk matrix, solve AX=B
        m, n, k = 3, 4, 2
        pivots = [0, 1, 3]
        rem = gen_row_echelon_matrix(m, n + k, pivots, 3)
        c = gen_glnz_matrix2(3, 3)
        ab = c * rem
        return ab[:,:n], ab[:,n:]
