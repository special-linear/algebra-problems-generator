from problem import Problem
from linear_algebra.common import *
import sympy as sp
from random import randint, choice, choices
import itertools as it
import functools as ft


def primitive(v):
    denom_lcm = ft.reduce(lambda x, y: sp.lcm(x, y), (x.as_numer_denom()[1] for x in v))
    u = tuple(x * denom_lcm for x in v)
    numer_gcd = ft.reduce(lambda x, y: sp.gcd(x, y), u)
    return sp.Matrix(*v.shape, [x // numer_gcd for x in u])


class EuclideanDistance(Problem):
    def __init__(self):
        self.x, self.us = self.gen_eucl_dist()

    def render(self):
        return 'Вычислить расстояние и угол между вектором $v$ и подпространством $\\langle {} \\rangle$, ' \
               'если\n\\[ v = {},\\qquad {}. \\]'.format(
            ', '.join('u_{{{}}}'.format(i + 1) for i in range(len(self.us))) if len(
                self.us) <= 3 else 'u_1,\\ldots,u_{{{}}}'.format(len(self.us)), matrix_to_tex(self.x), ',\\qquad '.join(
                'u_{} = {}'.format(i + 1, matrix_to_tex(u)) for i, u in enumerate(self.us)))
        # return 'Find the distance between a vector $v$ and a subspace $\\langle {} \\rangle$, ' \
        #        'where\n\\[ v = {},\\qquad {}. \\]'.format(
        #     ', '.join('u_{{{}}}'.format(i + 1) for i in range(len(self.us))) if len(
        #         self.us) <= 3 else 'u_1,\\ldots,u_{{{}}}'.format(len(self.us)), matrix_to_tex(self.x), ',\\qquad '.join(
        #         'u_{} = {}'.format(i + 1, matrix_to_tex(u)) for i, u in enumerate(self.us)))

    @staticmethod
    def gen_eucl_dist():
        flag = False
        entries_vals = list(it.chain(*[[i, -i] for i in range(1, 7)]))
        dim = 4
        while not flag:
            us = [sp.Matrix(choices(entries_vals, k=dim)) for _ in range(dim)]
            es = [us[0]]
            for i, u in enumerate(us[1:]):
                ebu = [bil(e, u) for e in es]
                if all(ebu):
                    ei = sum([-e*(bil(e, u)/bil(e, e)) for e in es], u)
                    if len([0 for x in ei if x != 0]) > 1 and (i < len(us) - 2 and all(x.as_numer_denom()[1] <= 3 for x in ei) or all(x.as_numer_denom()[1] == 1 for x in ei)):
                        es.append(ei)
                    else:
                        break
                else:
                    break
            else:
                flag = True
        return us[-1], us[:-1]

