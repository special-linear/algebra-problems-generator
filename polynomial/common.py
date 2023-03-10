import sympy as sp
from sympy.abc import x
from random import randint, choices


def random_poly(deg, coeffs_lim_lower, coeffs_lim_upper, lc_coeff_lim):
    return sp.Poly.from_list([randint(1, lc_coeff_lim), *choices(range(coeffs_lim_lower, coeffs_lim_upper + 1), k=deg)],
                             x)


def poly_to_tex(coeffs, variable='x'):
    monomials_strings = []
    deg = len(coeffs) - next((i for i, x in enumerate(coeffs) if x), None) - 1
    for i, c in enumerate(coeffs):
        monom_str = ''
        if i != deg:
            if c > 0 and i != 0:
                monom_str += '+'
            if c != 0:
                coeff_str = str(c) if c not in (1, -1) else str(c)[:-1]
                power = deg - i
                power_str = '^{{{}}}'.format(power) if power != 1 else ''
                monom_str += '{}{}{}'.format(coeff_str, variable, power_str)
        else:
            if c > 0 and deg != 0:
                monom_str += '+'
            if c != 0:
                monom_str += '{}'.format(str(c))
            if c == 0 and i == 0:
                monom_str += '0'
        monomials_strings.append(monom_str)
    return "".join(monomials_strings)


def complex_poly_to_tex(coeffs, variable='x'):
    monomials_strings = []
    deg = len(coeffs) - next((i for i, x in enumerate(coeffs) if x), None) - 1
    for i, c in enumerate(coeffs):
        monom_str = ''
        cr, ci = map(int, c.as_real_imag())
        if cr != 0 or ci != 0:
            coeff_str = ''
            if ci == 0:
                cr_str_raw = '{:+}'.format(cr) if i != 0 else str(cr)
                coeff_str += cr_str_raw if cr not in (1, -1) or i == deg else cr_str_raw[:-1]
            elif cr == 0:
                ci_str_raw = '{:+}'.format(ci) if i != 0 else str(ci)
                coeff_str += ci_str_raw if ci not in (1, -1) else ci_str_raw[:-1]
                coeff_str += 'i'
            else:
                if cr < 0 and ci < 0:
                    cr = -cr
                    ci = -ci
                    coeff_str += '-'
                elif i != 0:
                    monom_str += '+'
                if cr > 0:
                    ci_str_raw = '{:+}'.format(ci)
                    coeff_str += '({}{}i)'.format(cr, ci_str_raw if ci not in (1, -1) else ci_str_raw[:-1])
                else:
                    coeff_str += '({}i{})'.format(ci if ci != 1 else '', cr)
            power = deg - i
            power_str = '^{{{}}}'.format(power) if power not in (0, 1) else ''
            monom_str += '{}{}{}'.format(coeff_str, variable if i != deg else '', power_str)
        monomials_strings.append(monom_str)
    return "".join(monomials_strings)
