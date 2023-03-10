from problem import Problem
from linear_algebra.common import matrix_to_tex, gen_glnz_matrix2
from random import randint
import sympy as sp


class FGAbelianGroup(Problem):
    def __init__(self):
        self.gens, self.a = self.gen_fg_abelian_group()

    def render(self):
        return 'Абелева группа $G$ задана образующими и соотношениями ' \
               '$G = \\langle {0} \\mid A \\cdot ({0})^\\top \\rangle$, где\n\\[ A = {1}. \\]\n' \
               'Разложить $G$ в прямую сумму бесконечных ($\\mathbb{{Z}}$) и примарных ($\\mathbb{{Z}}_{{p^n}}$) ' \
               'циклических подгрупп и указать их образующие.'.format(
            ', '.join(self.gens), matrix_to_tex(self.a)
        )

    @staticmethod
    def gen_fg_abelian_group():
        d = sp.zeros(4, 5)
        good_a = False
        while not good_a:
            c = randint(2, 4)
            for i in range(3):
                c *= randint(1, i + 3)
                d[i,i] = c
            u, v = gen_glnz_matrix2(4, entries_lim=5), gen_glnz_matrix2(5, entries_lim=4)
            a = u * d * v
            good_a = all(abs(x) < 200 for x in a)
        return 'abcde', a
