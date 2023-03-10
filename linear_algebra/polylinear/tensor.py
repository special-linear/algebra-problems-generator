from problem import Problem
from linear_algebra.common import *


class TensorExpandSL2BorelCommutator(Problem):
    def __init__(self):
        self.basis = self.gen_basis()

    def render(self):
        return 'Рассмотрим пространство\n\\[ V = \\left\\{{ ' \
               '\\begin{{pmatrix}} a & b \\\\ 0 & -a \\end{{pmatrix}} ' \
               '\\,\\middle|\\, a,b\\in\\mathbb{{C}} \\right\\}}, \\]\n' \
               'и рассмотрим бинарную операцию\n' \
               '\\[ X,Y \\longmapsto XY-YX. \\]\n' \
               'Представьте ее как тензор валентности $(1,2)$ и разложите по базису\n' \
               '\\[ {}. \\]'.format(
            ', \\quad '.join(
                'e_{{{}}} = \\begin{{pmatrix}} {} & {} \\\\ 0 & {} \\end{{pmatrix}}'.format(i + 1, v[0], v[1], -v[0])
                for i, v in enumerate(self.basis))
        )
        # return 'Consider a vector space\n\\[ V = \\left\\{{ ' \
        #        '\\begin{{pmatrix}} a & b \\\\ 0 & -a \\end{{pmatrix}} ' \
        #        '\\,\\middle|\\, a,b\\in\\mathbb{{C}} \\right\\}}, \\]\n' \
        #        'and a binary operation\n' \
        #        '\\[ X,Y \\longmapsto XY-YX. \\]\n' \
        #        'Present it as a tensor of type $(1,2)$ and find its expansion with respect to a basis\n' \
        #        '\\[ {}. \\]'.format(
        #     ', \\quad '.join(
        #         'e_{{{}}} = \\begin{{pmatrix}} {} & {} \\\\ 0 & {} \\end{{pmatrix}}'.format(i + 1, v[0], v[1], -v[0])
        #         for i, v in enumerate(self.basis))
        # )

    @staticmethod
    def gen_basis():
        m = gen_glnz_matrix2(2, entries_lim=4)
        return tuple(m[:, 0]), tuple(m[:, 1])
