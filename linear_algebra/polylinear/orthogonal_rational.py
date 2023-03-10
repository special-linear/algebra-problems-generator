from problem import Problem

from linear_algebra.common import *

from random import choice, randint


class OrthogonalCanonicalForm(Problem):
    def __init__(self):
        self.matrix = self.gen_orth_matrix()

    def render(self):
        return 'Найти каноническую форму и канонический базис ортогонального оператора, ' \
               'заданного в некотором ортонормированном базисе матрицей\n' \
               '\\[ {}. \\]'.format(
            matrix_to_tex(self.matrix)
        )

    @staticmethod
    def gen_orth_matrix():
        init_lim = 2
        rot_m = choice([
            sp.Matrix([[sp.Rational(3, 5), sp.Rational(-4, 5)], [sp.Rational(4, 5), sp.Rational(3, 5)]]),
            sp.Matrix([[sp.Rational(-3, 5), sp.Rational(-4, 5)], [sp.Rational(4, 5), sp.Rational(-3, 5)]]),
            sp.Matrix([[sp.Rational(3, 5), sp.Rational(4, 5)], [sp.Rational(-4, 5), sp.Rational(3, 5)]])
        ])
        matrix_is_good = False
        while not matrix_is_good:
            antisym_m = sp.Matrix(4, 4,
                              lambda i, j: sp.Rational(randint(-init_lim, init_lim), randint(1, init_lim)) if i < j else 0)
            antisym_m = antisym_m - antisym_m.transpose()
            orth_m = skewsym2orth(antisym_m)
            matrix_is_good = all(orth_m) and all(3 < x.as_numer_denom()[1] < 13 for x in orth_m)
        return orth_m.transpose() * sp.Matrix(sp.BlockDiagMatrix(rot_m, sp.diag(-1, -1))) * orth_m