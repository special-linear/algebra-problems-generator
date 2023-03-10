from problem import Problem
from linear_algebra.common import *
import sympy as sp
from random import randint


class AffineSubspaceEquation(Problem):
    def __init__(self):
        self.vectors = self.gen_vectors()

    def render(self):
        return 'Рассмотрим наименьшее возможное аффинное подпространство $\\mathcal{{A}}\\subseteq\\mathbb{{R}}^4$, ' \
               'содержащее векторы\n\\[ {} \\]\n' \
               'Найдите уравнения (на координаты векторов), задающие элементы $\\mathcal{{A}}$. ' \
               'Иными словами, найдите такую матрицу $A$ и такой столбец $b$, что\n' \
               '\\[ \\mathcal{{A}} = \\{{ v \\mid Av=b \\}}. \\]'.format(
            ',\\ '.join('v_{{{}}} = {}'.format(i + 1, vector2tex(v)) for i, v in enumerate(self.vectors))
        )

    @staticmethod
    def gen_vectors():
        flag = False
        while not flag:
            a = sp.Matrix([[choice((-1, 1)) * randint(1, 3) for i in range(2)] for j in range(2)])
            ugm = sp.Matrix([sp.eye(2), -a])
            ugm = ugm.col_insert(3, ugm[:,0] + ugm[:,1])
            c = gen_glnz_matrix2(3)
            ugm = ugm * c
            shift = sp.Matrix([[choice((1, -1)) * randint(1, 3)] for _ in range(4)])
            vs = sp.Matrix([[shift]*3]) + ugm
            flag = all(abs(x) < 10 for x in vs) and sp.Matrix([[ugm, shift]]).rank() == 3
        return tuple(shift), *[tuple(vs[:, i]) for i in range(3)]
