from problem import Problem
from list_problem import FromListProblem
import sympy as sp
import itertools as it
import more_itertools as mit
from linear_algebra.common import *
from random import sample


class GeneratingSubset(Problem):
    def __init__(self):
        self.columns = self.gen_generating_subset()

    def render(self):
        return 'Дан следующий набор векторов:\n' \
               '\\[ {}. \\]\n' \
               'Выделите в этом наборе элементы базиса порождаемого ими подпространства.'.format(
            ', \\quad '.join(matrix_to_tex(self.columns[:,i]) for i in range(self.columns.shape[1])
            )
        )
        # return 'Consider the following set of vectors:\n' \
        #        '\\[ {}. \\]\n' \
        #        'Find a subset that form a basis of the subspace spanned by these vectors.'.format(
        #     ', \\quad '.join(matrix_to_tex(self.columns[:, i]) for i in range(self.columns.shape[1])
        #                      )
        # )

    @staticmethod
    def gen_generating_subset():
        rem = gen_row_echelon_matrix(5, 7, [0, 1, 3, 6], 3)
        c = gen_glnz_matrix2(5, 3)
        return c * rem


class LinearIndependenceFunctions(FromListProblem):
    problems = [
        'Установите точные условия на набор чисел $c_1,\\ldots,c_m,d_1,\\ldots,d_n\\in\\mathbb{R}$, при которых набор '
        'функций $f_i=\\max(0,x-c_i)$, $g_j=\\max(0,d_i-x)$ линейно независим '
        'в пространстве непрерывных функций на $\\mathbb{R}$',

        'Установите точные условия на набор чисел $a_1<b_1,\\ldots,a_n<b_n\\in\\mathbb{R}$, при которых набор функций '
        '$f_i=\\max(a_i, \\min(x, b_i))$ линейно независим в пространстве непрерывных функций на $\\mathbb{R}$.',

        'Установите точные условия на набор чисел $a_1<b_1,\\ldots,a_n<b_n\\in\\mathbb{R}$, при которых набор '
        'характеристических функций полуинтервалов $[a_i,b_i)$ линейно независим '
        'в пространстве функций на $\\mathbb{R}$.',

        'Установите точные условия на набор чисел $a_1,\\ldots,a_n,c_1,\\ldots,c_n\\in\\mathbb{R}$, при которых набор '
        'функций $f_i=a_i+\\max(0,x-c_i)$ линейно независим в пространстве непрерывных функций на $\\mathbb{R}$.',

        'Установите точные условия на набор чисел $a_1,\\ldots,a_n,c_1,\\ldots,c_n\\in\\mathbb{R}$, при которых набор '
        'функций $f_i=a_i+\\chi_{[c_i,+\\infty)}$, где $\\chi_A$ это характеристическая функция множества $A$, '
        'линейно независим в пространстве функций на $\\mathbb{R}$.',
    ]


class LinearIndependencePolyTrigExp(Problem):
    def __init__(self):
        self.basis, self.coeffs = self.gen_linearly_independend_poly_trig_exp()

    def render(self):
        return 'Докажите линейную независимость набора функций\n\\begin{{align}} {}. \\end{{align}}'.format(
            ' \\\\ '.join(
                '& f_{{{}}} = '.format(i)
                + ''.join(
                    '{}{}'.format(
                        '{:+}'.format(c) if c not in (1, -1) else '-' if c == -1 else '+',
                        f
                    ) for c, f in zip(row, self.basis) if c
                ).strip('+') for i, row in enumerate(self.coeffs)
            )
        )

    @staticmethod
    def gen_linearly_independend_poly_trig_exp():
        num_poly = 2
        num_trig = 2
        num_exp = 2
        num_func_total = num_poly + num_trig + num_exp
        dim = 4
        basis = ordered_sample(['x', 'x^2', 'x^3'], k=num_poly)
        basis += ordered_sample(['\\sin(x)', '\\cos(x)', '\\sin(2x)', '\\cos(2x)'], k=num_trig)
        basis += ordered_sample(['\\exp(x)', '\\exp(-x)', '\\exp(2x)', '\\exp(-2x)'], k=num_exp)
        good_coeffs = False
        while not good_coeffs:
            coeffs = gen_sparse_glnq_matrix(num_func_total)[:dim,:]
            good_coeffs = all(2 <= mit.ilen(filter(bool, coeffs.row(i))) <= 4 for i in range(dim))\
                          and all(any(coeffs.col(j)) for j in range(num_func_total))
        for i in range(dim):
            row = coeffs.row(i)
            if next(c for c in row if c) < 0:
                row = -row
            row /= sp.gcd_list(list(row))
            coeffs[i,:] = row
        return tuple(basis), tuple(tuple(map(int, coeffs.row(i))) for i in range(dim))


def ordered_sample(population, k):
    indices = sample(range(len(population)), k=k)
    return [population[i] for i in sorted(indices)]
