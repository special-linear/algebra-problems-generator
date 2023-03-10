from problem import Problem
import sympy as sp
from linear_algebra.common import matrix_to_tex
from random import randint, choice
import more_itertools as mit


class QuadFormSignature(Problem):
    def __init__(self):
        self.b = self.generate()

    def render(self):
        return 'Квадратичная форма имеет матрицу Грама\n\\[ {}. \\]\nКаковы ее индексы инерции?'.format(
            matrix_to_tex(self.b)
        )

    @staticmethod
    def generate():
        corner_minors = [0]
        size = 3
        while not all(corner_minors) and not all(x > 0 for x in corner_minors):
            b = sp.Matrix(size, size, lambda i, j: choice((1, -1)) * randint(1, 4) if i < j else 0)
            b += b.transpose() + sp.diag(*[choice((1, -1)) * randint(1, 4) for _ in range(size)])
            corner_minors = [int(b[:i,:i].det()) for i in range(size + 1)]
        return sp.ImmutableMatrix(b)
