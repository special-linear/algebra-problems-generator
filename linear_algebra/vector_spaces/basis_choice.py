from problem import Problem
from list_problem import FromListProblem
from numbertheory.gaussint import GaussInt
from random import randint, choice


class BasisChoicePolynomials(Problem):
    def __init__(self):
        self.points = self.gen_basis_choice_polynomial()

    def render(self):
        return 'Рассмотрим векторное пространство\n' \
               '\\[ V = \\{{ f \\in\\mathbb{{R}}[x] \\mid \\deg(f)\\leqslant 7,\\  f({}) = f({}) = 0\\}} \\]\n' \
               'над полем $\\mathbb{{R}}$. Найдите его базис и докажите, что это действительно базис.'.format(
            *self.points
        )

    @staticmethod
    def gen_basis_choice_polynomial():
        complex_point = GaussInt(choice((1, -1)) * randint(1, 3), choice((1, -1)) * randint(2, 4))
        real_point = choice((1, -1)) * randint(1, 3)
        return complex_point, real_point


class BasisChoiceAntisymmComplexMatrices(Problem):
    def __init__(self):
        self.vector = self.gen_vector()

    def render(self):
        return 'Рассмотрим векторное пространство\n' \
               '\\[ V = \\left\\{{ A\\in\\operatorname{{M}}(3,\\mathbb{{C}}) \\,\\middle|\\, ' \
               'A^\\top=-A,\\ A\\cdot {}^\\top \\in \\mathbb{{R}}^3 \\right\\}} \\]\n' \
               'над полем $\\mathbb{{R}}$. Найдите его базис и докажите, что это действительно базис.'.format(
            self.vector
        )
        # return 'Consider the vector space\n' \
        #        '\\[ V = \\left\\{{ A\\in\\operatorname{{M}}(3,\\mathbb{{C}}) \\,\\middle|\\, ' \
        #        'A^\\top=-A,\\ A\\cdot {}^\\top \\in \\mathbb{{R}}^3 \\right\\}} \\]\n' \
        #        'over the field $\\mathbb{{R}}$. Find a basis of $V$ and prove that this is indeed a basis.'.format(
        #     self.vector
        # )

    @staticmethod
    def gen_vector():
        return tuple(choice((1, -1)) * randint(1, 4) for _ in range(3))
