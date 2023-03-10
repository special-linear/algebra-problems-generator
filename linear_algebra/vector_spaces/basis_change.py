import itertools

from problem import Problem
from linear_algebra.common import *
from numbertheory.gaussint import GaussInt
import numpy as np

class BasisChangeComplexPoly(Problem):
    def __init__(self):
        self.space, self.a, self.b = self.gen_basis_change()

    def render(self):
        return 'Рассматривается векторное пространство\n\\[{}\\]\nнад полем $\mathbb{{R}}$. В нем заданы два базиса:\n' \
               '\\begin{{center}}\n' \
               '\\begin{{tabular}}{{c@{{\qquad}}c}}\n' \
               '$a = {{}}$ & $b =  {{}}$\\\\\n' \
               '$\\begin{{array}}{{l}}{}\end{{array}}$ &\n' \
               '$\\begin{{array}}{{l}}{}\end{{array}}$\n' \
               '\end{{tabular}}\n' \
               '\end{{center}}\n' \
               'Найти матрицу перехода между базисами $a$ и $b$.'.format(
            self.vector_spaces[self.space]['desc'], ',\\\\'.join(self.a), ',\\\\'.join(self.b)
        )
        # return 'Consider the vector space\n\\[{}\\]\n over the field $\mathbb{{R}}$. There the following two bases are chosen:\n' \
        #        '\\begin{{center}}\n' \
        #        '\\begin{{tabular}}{{c@{{\qquad}}c}}\n' \
        #        '$a = {{}}$ & $b =  {{}}$\\\\\n' \
        #        '$\\begin{{array}}{{l}}{}\end{{array}}$ &\n' \
        #        '$\\begin{{array}}{{l}}{}\end{{array}}$\n' \
        #        '\end{{tabular}}\n' \
        #        '\end{{center}}\n' \
        #        'Find the matrix of the basis change from $a$ to $b$.'.format(
        #     self.vector_spaces[self.space]['desc'], ',\\\\'.join(self.a), ',\\\\'.join(self.b)
        # )

    vector_spaces = {
        'f0f1': {
            'dim': 4,
            'desc': "\\{{ f\in\mathbb{{C}}[t] \mid \deg(f)\leqslant2,\ f(0), f(1)\in\mathbb{{R}} \\}}",
        },
        'f0fm1': {
            'dim': 4,
            'desc': "\\{{ f\in\mathbb{{C}}[t] \mid \deg(f)\leqslant2,\ f(0), f(-1)\in\mathbb{{R}} \\}}",
        }
    }

    @staticmethod
    def gen_basis_change():
        space = choice(list(BasisChangeComplexPoly.vector_spaces.keys()))
        cea = gen_glnz_matrix(4)
        cbe = gen_glnz_matrix(4)
        a, b = map(lambda m: ['+'.join(map(''.join,
                                           list(zip([str(m[0, j]),
                                                     '({})'.format(
                                                         GaussInt(m[1, j], m[3, j] * (-1 if space == 'f0f1' else 1))),
                                                     '({})'.format(GaussInt(m[2, j], m[3, j]))
                                                     ], ['', '\cdot t', '\cdot t^2']))))
                              for j in range(4)],
                   [cea, cbe])
        return space, a, b


class BasisChangeGF3Subspace(Problem):
    def __init__(self):
        self.b1, self.b2  = self.gen_basis_change()

    def render(self):
        return 'В векторном пространстве $\mathbb{{F}}_3^6$ столбцов высоты $6$ ' \
               'над полем из трех элементов $\mathbb{{F}}_3 = \mathbb{{Z}}/3\mathbb{{Z}}$ ' \
               'рассматривается подпространство размерности $5$, для которого ' \
               'следующие два набора векторов являются базисами:\n' \
               '\\[ f \colon {}; \qquad g \colon {}. \\]\n' \
               'Найти матрицу перехода от базиса $f$ к базису $g$.'.format(
            ',\ '.join(map(matrix_to_tex, self.b1)), ',\ '.join(map(matrix_to_tex, self.b2))
        )

    @staticmethod
    def gen_basis_change():
        if choice((1, -1)) == 1:
            e1 = [1, 2, 0, 0, 0, 0]
            e2 = [1, 0, 2, 0, 0, 0]
            e3 = [1, 0, 0, 1, 0, 1]
            e4 = [1, 0, 0, 0, 1, 0]
            e5 = [1, 0, 0, 0, 0, 1]
        else:
            e1 = [1, 1, 0, 0, 0, 0]
            e2 = [1, 0, -1, 0, 0, 0]
            e3 = [1, 0, 0, 1, 0, 0]
            e4 = [1, 0, 0, 0, -1, 0]
            e5 = [1, 0, 0, 0, 0, 1]
        es = [np.matrix(x).transpose() for x in [e1, e2, e3, e4, e5]]
        flag = False
        mod3 = np.vectorize(lambda x: x % 3)
        while not flag:
            c1 = gen_glzmz_matrix(5, modulo=3)
            c2 = gen_glzmz_matrix(5, modulo=3)
            b1 = tuple(mod3(sum(c1[i, j] * es[j] for j in range(5))) for i in range(5))
            b2 = tuple(mod3(sum(c2[i, j] * es[j] for j in range(5))) for i in range(5))
            flag = len({tuple(v.transpose().flat) for v in itertools.chain(b1, b2)}) == 10
        return b1, b2
