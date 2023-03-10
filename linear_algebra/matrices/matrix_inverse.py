from problem import Problem
from linear_algebra.common import *
import sympy as sp
from sympy.abc import x


class MatrixInverse(Problem):
    def __init__(self):
        self.a = self.gen_matrix_inverse()

    def render(self):
        return 'Найти матрицу, обратную к матрице\n\\[ {}. \\]'.format(matrix_to_tex(self.a))
        # return 'Find the inverse of the matrix\n\\[ {}. \\]'.format(matrix_to_tex(self.a))

    @staticmethod
    def gen_matrix_inverse():
        return gen_glnz_matrix2(4, 4)
