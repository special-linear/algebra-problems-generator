from problem import Problem
from linear_algebra.common import *
import sys


class SVDSmall(Problem):
    def __init__(self):
        self.a = self.gen_svd()

    def render(self):
        return 'Пусть задана матрица\n' \
               '\\[ A = {}. \\]\n' \
               'Найдите\n' \
               '\\begin{{enumerate}}\n' \
               '\\item Ее сингулярное разложение;\n' \
               '\\item Числа обусловленности $K_1(A)$, $K_2(A)$, $K_\\infty(A)$;\n' \
               '\\item Ближайшую к $A$ матрицу ранга $1$.\n' \
               '\\end{{enumerate}}'.format(matrix_to_tex(self.a))

    @staticmethod
    def gen_svd():
        init_lim = 9
        sizes = (2, 2)
        matrix_is_good = False
        while not matrix_is_good:
            pq_are_good = False
            while not pq_are_good:
                pq = []
                for m in sizes:
                    matrix_is_good = False
                    while not matrix_is_good:
                        antisym_m = sp.Matrix(m, m,
                                              lambda i, j: sp.Rational(randint(-init_lim, init_lim),
                                                                       randint(1, init_lim)) if i < j else 0)
                        antisym_m = antisym_m - antisym_m.transpose()
                        orth_m = skewsym2orth(antisym_m)
                        matrix_is_good = all(orth_m) and all(5 <= x.as_numer_denom()[1] < 50 for x in orth_m)
                    pq.append(orth_m)
                p_denom, q_denom = (sp.lcm_list([x.as_numer_denom()[1] for x in p]) for p in pq)
                pq_are_good = p_denom != q_denom
            total_denom = sp.lcm_list([x.as_numer_denom()[1] for p in pq for x in p])
            matrix_is_good = False
            count = 100
            while not matrix_is_good and count:
                count -= 1
                sigma = sp.Matrix(*sizes, lambda i, j: total_denom * choice((1, -1)) * randint(2, 9) if i == j else 0)
                a = pq[0] * sigma * pq[1]
                total_denom = sp.lcm_list([x.as_numer_denom()[1] for x in a])
                matrix_is_good = abs(sigma[0, 0]) < 500 and abs(sigma[1, 1]) < 500 and abs(sigma[0, 0]) != abs(
                    sigma[1, 1]) and all(500 > abs(x) >= 5 for x in a) and total_denom == 1
        return a

