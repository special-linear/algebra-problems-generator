from problem import Problem
from linear_algebra.common import *
from random import randint


class DiagonalizableRecurrent(Problem):
    def __init__(self):
        self.a = self.gen_diagonalizable_recurrent()

    def render(self):
        return 'Для различных начальных $v_0$ рассмотрим последовательность векторов\n' \
               '\\[ v_{{n+1}} = Av_n,\\quad\\text{{где}}\\quad A = {}. \\]\n' \
               'Найдите собственные числа и собственные векторы $A$. При каких $v_0$ в получающейся ' \
               'последовательности с некоторого момента первая координата положительна?'.format(matrix_to_tex(self.a))

    @staticmethod
    def gen_diagonalizable_recurrent():
        flag = False
        while not flag:
            min_ev = -randint(1, 3)
            max_ev = randint(-min_ev + 1, 6)
            d = sp.Matrix([[max_ev, 0], [0, min_ev]])
            c = gen_glnz_matrix2(2, entries_lim=6)
            a = c.inv() * d * c
            flag = all(0 < abs(x) < 15 for x in a)
        return a
