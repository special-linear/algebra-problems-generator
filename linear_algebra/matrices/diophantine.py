from problem import Problem
from linear_algebra.common import gen_glnz_matrix2, linear_system_tex
from random import randint
import sympy as sp


class LinearDiophantineSystem(Problem):
    def __init__(self):
        self.a, self.b = self.gen_linear_diophantine()

    def render(self):
        return 'Решить в целых числах систему уравнений\n\\[ {}. \\]'.format(
            linear_system_tex(self.a, self.b, 'xyzwt')
        )

    @staticmethod
    def gen_linear_diophantine():
        m, n = 4, 5
        d = sp.zeros(m, n)
        b = sp.zeros(m, 1)
        good_a = False
        while not good_a:
            c = 1
            for i in range(m-1):
                d[i,i] = c
                b[i] = c * randint(2, 5)
                c *= randint(1, i + 3)
            u, v = gen_glnz_matrix2(m, entries_lim=5), gen_glnz_matrix2(n, entries_lim=4)
            a = u * d * v
            good_a = all(abs(x) < 200 for x in a)
        return tuple(map(tuple, a.tolist())), tuple(u * b)
