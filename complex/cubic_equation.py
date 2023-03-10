from problem import Problem
from random import randint
import sympy as sp
from sympy import I, QQ
from sympy.abc import x


def gen_nonzero_gaussint(values_lim):
    a = (0, 0)
    while a == (0, 0):
        a = tuple(randint(-values_lim, values_lim) for _ in range(2))
    return a[0] + I * a[1]


def complex_str(z):
    a, b = z.as_real_imag()
    if b != 0:
        if b == 1:
            imag_str = 'i'
        elif b == -1:
            imag_str = '-i'
        else:
            imag_str = '{}i'.format(b)
    else:
        imag_str = ''
    return ''.join((str(a) if a != 0 else '', '+' if a != 0 and b > 0 else '', imag_str))


def complex_pars(z):
    return ('{}' if sp.re(z) == 0 or sp.im(z) == 0 else '({})').format(complex_str(z))


def complex_poly_str(coeffs):
    monoms_strs = []
    for i, c in enumerate(reversed(coeffs)):
        if c:
            power = ('x^{}'.format(i) if i > 1 else 'x') if i else ''
            c_str = complex_pars(c) if c not in (1, -1) else complex_str(c)[:-1]
            # print(c, c_str)
            monom_str = '{}{}{}'.format('+' if c_str and c_str[0] != '-' else '', c_str, power)
            monoms_strs.append(monom_str)
    return ''.join(reversed((monoms_strs)))



class CubicEquation(Problem):
    def __init__(self):
        self.f = self.gen_cubic_equation()

    def render(self):
        return 'Решить кубическое уравнение\n\\[ {} = 0. \\]'.format(complex_poly_str(self.f))
        # return 'Solve the cubic equation\n\\[ {} = 0. \\]'.format(complex_poly_str(self.f))

    @staticmethod
    def gen_cubic_equation():
        good_poly = False
        while not good_poly:
            z1, z2, z3 = (gen_nonzero_gaussint(5) for _ in range(3))
            f = sp.Poly((x - z1) * (x - z2) * (x - z3), domain='QQ(I)')
            f_red = sp.compose(f, x - f.all_coeffs()[1] / 3, domain='QQ(I)')
            f_red_coeffs = f_red.all_coeffs()
            p = f_red_coeffs[-2]
            q = f_red_coeffs[-1]
            # good_poly = True
            if not q:
                continue
            r = sp.sqrt(p**3 / 27 + q**2 / 4)
            w = sp.simplify(-q / 2 + r)
            w_re, w_im = w.as_real_imag()
            if w_re.is_rational and w_im.is_rational and (w_re == 0 or abs(w_re) == abs(w_im)):
                wr = sp.root(w, 3)
                wr_re, wr_im = wr.as_real_imag()
                if wr_re.is_rational and wr_im.is_rational and not (wr_re.is_integer and wr_im.is_integer):
                    good_poly = True
        return f.all_coeffs()

