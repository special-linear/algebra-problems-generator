from problem import Problem
import sympy as sp
import itertools as it
from random import choices
from polynomial.common import poly_to_tex


class FiniteFieldMultiplication(Problem):
    def __init__(self):
        self.p, self.deg, self.f, self.beta, self.gamma = self.generate()

    def render(self):
        return 'Многочлен $f = {0} \\in\\mathbb{{F}}_{{{1}}}[x]$ неприводим. ' \
               'Рассмотрим поле $F = \\mathbb{{F}}_{{{1}}}[x]/(f)$. Обозначим $\\alpha=[x]$, тогда ' \
               '$F$ имеет как векторное пространство над $\\mathbb{{F}}_{{{1}}}$ ' \
               'базис $1,\\alpha,{2}$. Чему равно (в этом базисе) ' \
               'произведение $\\beta\\cdot\\gamma$, где\n\\[ \\beta = {3}, \\qquad \\gamma = {4}? \\]'.format(
            poly_to_tex(self.f),
            self.p,
            ','.join('\\alpha^{{{}}}'.format(i) for i in range(2, self.deg)),
            poly_to_tex(self.beta, variable='\\alpha'),
            poly_to_tex(self.gamma,variable='\\alpha')
        )

    @staticmethod
    def generate():
        x = sp.symbols('x')
        p = 3
        deg = 4
        flag = False
        while not flag:
            f = sp.Poly.from_list(tuple(it.chain((1,), choices(range(p), k=deg))), x, modulus=p)
            flag = f.is_irreducible
        flag = False
        while not flag:
            beta, gamma = (sp.Poly.from_list(tuple(it.chain((0,), choices(range(p), k=deg))), x, modulus=p) for _ in range(2))
            flag = (beta * gamma).degree() > deg and beta != gamma
        return p, deg, tuple(f.as_list()), tuple(beta.as_list()), tuple(gamma.as_list())


class FiniteFieldInversion(Problem):
    def __init__(self):
        self.p, self.deg, self.f, self.beta = self.generate()

    def render(self):
        return 'Многочлен $f = {0} \\in\\mathbb{{F}}_{{{1}}}[x]$ неприводим. ' \
               'Рассмотрим поле $F = \\mathbb{{F}}_{{{1}}}[x]/(f)$. Обозначим $\\alpha=[x]$, тогда ' \
               '$F$ имеет как векторное пространство над $\\mathbb{{F}}_{{{1}}}$ ' \
               'базис $1,\\alpha,{2}$. Выразите в этом базисе элемент $\\beta^{{-1}}$, обратный к $\\beta={3}$.'.format(
            poly_to_tex(self.f),
            self.p,
            ','.join('\\alpha^{{{}}}'.format(i) for i in range(2, self.deg)),
            poly_to_tex(self.beta, variable='\\alpha')
        )

    @staticmethod
    def generate():
        x = sp.symbols('x')
        p = 2
        deg = 4
        flag = False
        while not flag:
            f = sp.Poly.from_list(tuple(it.chain((1,), choices(range(p), k=deg))), x, modulus=p)
            flag = f.is_irreducible
        flag = False
        while not flag:
            beta, gamma = (sp.Poly.from_list(tuple(it.chain((0,), choices(range(p), k=deg))), x, modulus=p) for _ in
                           range(2))
            flag = beta.degree() > 1
        return p, deg, tuple(f.as_list()), tuple(beta.as_list())