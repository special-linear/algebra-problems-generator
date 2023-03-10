from problem import Problem
from random import randint
from numbertheory.gaussint import GaussInt
import math


def gen_nonzero_gaussint(values_lim):
    a = (0, 0)
    while a == (0, 0):
        a = tuple(randint(-values_lim, values_lim) for _ in range(2))
    return GaussInt(*a)


def complex_pars(z):
    return ('{}' if z.r == 0 or z.i == 0 else '({})').format(z)


def complex_affine(a, b):
    a_str = complex_pars(a) if a not in (GaussInt(1), GaussInt(-1)) else str(a)[:-1]
    b_str = str(b)
    return ('{}z+{}' if b_str[0] != '-' else '{}z{}').format(a_str, b_str)


class MoebiusTransformation(Problem):
    def __init__(self):
        self.f, self.line1, self.line2, self.circle1, self.circle2 = self.gen_moebius_transformation()

    def render(self):
        figures = [
            'прямая $\\operatorname{{Re}}\\big({} \\cdot z\\big) = {}$'.format(complex_pars(self.line1[0]), self.line1[1]),
            'прямая $|{}-z| = |{}-z|$'.format(*self.line2),
            'круг $|{}-z|\\leqslant {}$'.format(*self.circle1),
            'круг $|{}-z|\\leqslant {}$'.format(*self.circle2)
        ]
        # figures = [
        #     'the line $\\operatorname{{Re}}\\big({} \\cdot z\\big) = {}$'.format(complex_pars(self.line1[0]),
        #                                                                        self.line1[1]),
        #     'the line $|{}-z| = |{}-z|$'.format(*self.line2),
        #     'the circle $|{}-z|\\leqslant {}$'.format(*self.circle1),
        #     'the circle $|{}-z|\\leqslant {}$'.format(*self.circle2)
        # ]
        return 'Задано дробно-линейное преобразование\n' \
               '\\[ f(x) = \\frac{{{}}}{{{}}}. \\]\n' \
               'Найти образы и прообразы под действием $f$ следующих объектов:\n' \
               '\\begin{{enumerate}}\n{}.\n\\end{{enumerate}}'.format(
            complex_affine(self.f[0], self.f[1]),
            complex_affine(self.f[2], self.f[3]),
            ';\n'.join('\\item {}'.format(fig) for fig in figures)
        )
        # return 'The following M\\"{{o}}bius transformation is given:\n' \
        #        '\\[ f(x) = \\frac{{{}}}{{{}}}. \\]\n' \
        #        'Find the images and the preimages under $f$ for the following figures:\n' \
        #        '\\begin{{enumerate}}\n{}.\n\\end{{enumerate}}'.format(
        #     complex_affine(self.f[0], self.f[1]),
        #     complex_affine(self.f[2], self.f[3]),
        #     ';\n'.join('\\item {}'.format(fig) for fig in figures)
        # )

    @staticmethod
    def gen_moebius_transformation():
        values_lim = 3
        a, b, c, d = 0, 0, 0, 0
        while not a * d - b * c:
            a, b = (gen_nonzero_gaussint(values_lim) for _ in range(2))
            c, d = 0, GaussInt(0, 0)
            while not d or d.norm() > values_lim**2:
                c, d = (gen_nonzero_gaussint(values_lim) for _ in range(2))
                z0 = d
                d *= c
        alpha = gen_nonzero_gaussint(3)
        beta = (alpha * z0).r
        z1, z2 = z0, z0
        while z1 == z2 or (z1-z0).norm() != (z1-z0).norm():
            z1, z2 = (gen_nonzero_gaussint(3) for _ in range(2))
        c1, r1 = 0, 0
        while not c1 or (c1 - z0).norm() != r1**2:
            c1 = gen_nonzero_gaussint(3) + z0
            r1 = int(math.sqrt((c1 - z0).norm()))
        c2, r2 = GaussInt(0), 0
        while not c1 or c2 == c1 or (c2 - z0).norm() != r2**2:
            c2 = gen_nonzero_gaussint(3) + z0
            r2 = int(math.sqrt((c2 - z0).norm()))
        r2 += 1
        return (a, b, c, d), (alpha, beta), (z1, z2), (c1, r1), (c2, r2)


