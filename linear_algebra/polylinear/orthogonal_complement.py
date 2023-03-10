from problem import Problem
import sympy as sp
from random import randint, choice
from linear_algebra.common import matrix_to_tex


class OrthogonalComplementMatricesSymmetricTraceZero(Problem):
    def __init__(self):
        self.u, self.v = self.gen_orthogonal_complement()

    def render(self):
        return 'Consider the real vector space\n' \
               '\\[ V = \\{{ A \\in M(2,\\mathbb{{R}}) \\mid A=A^\\top,\ \\operatorname{{tr}}(A)=0 \\}} \]\n' \
               'equipped with a scalar product $(A,B) = \\operatorname{{tr}}(AB^\\top)$. ' \
               'Find the orthogonal complement of a subspace\n' \
               '\\[ U = \\{{ A\\in V \\mid A\\cdot {}^\\top = 0 \\}} \\]\n' \
               'and the projection onto $U$ of the vector\n' \
               '\\[ v = {}. \\]'.format(
            self.u, matrix_to_tex(self.v)
        )

    @staticmethod
    def gen_orthogonal_complement():
        sign = choice((1, -1))
        u = (0, 0, 0)
        while abs(u[0]) == abs(u[1]):
            u = (sign * randint(1, 3), -sign * randint(1, 3),  0)
        u_vec = sp.Matrix(3, 1, u)
        v = sp.zeros(3, 3)
        z = sp.zeros(3, 1)
        while v.trace() != 0 or v @ u_vec == z:
            v = sp.Matrix(3, 3, lambda i, j: randint(-1, 1))
            v = v + v.transpose()
        return u, v
