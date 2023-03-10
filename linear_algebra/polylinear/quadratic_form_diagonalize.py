from problem import Problem
from random import choices
from linear_algebra.common import *


class QuadFormDiagPolynomialsIntegral(Problem):
    def __init__(self):
        self.lower_limit, self.upper_limit, self.weight = self.gen_quad_form_diag_polynomials()

    def render(self):
        a, b = self.weight
        if a > 0:
            weight_str = '({}x{}{})'.format(a if a > 1 else '', '+' if b > 0 else '-', abs(b))
        else:
            weight_str = '({}{}x)'.format(b, a)
        return 'На пространстве многочленов $\\mathbb{{R}}[x]_{{\\leqslant 2}}$ степени не выше $2$ ' \
               'задана билинейная форма $B$ по правилу\n' \
               '\\[ B(f, g) = \\int_{{{}}}^{{{}}} {}\\cdot f(x)\\cdot g(x) \\operatorname{{d}}\\!x \\]\n' \
               'Диагонализируйте форму $B$ и предъявите соответствующий базис из многочленов.'.format(
            self.lower_limit, self.upper_limit, weight_str
        )
        # return 'On the vector space $\\mathbb{{R}}[x]_{{\\leqslant 2}}$ of polynomials of degree at most $2$ ' \
        #        'the bilinear form $B$ is given by\n' \
        #        '\\[ B(f, g) = \\int_{{{}}}^{{{}}} {}\\cdot f(x)\\cdot g(x) \\operatorname{{d}}\\!x \\]\n' \
        #        'Diagonalize this form via Lagrange method and write down ' \
        #        'the corresponding basis of polynomials.'.format(
        #     self.lower_limit, self.upper_limit, weight_str
        # )

    @staticmethod
    def gen_quad_form_diag_polynomials():
        x = sp.symbols('x')
        basis = [1, x, x**2]
        entries_vals = list(range(1, 5))
        limits_vals = list(range(-3, 4))
        flag = False
        while not flag:
            lower_limit, upper_limit = sorted(sample(limits_vals, k=2))
            weight = choices(entries_vals, k=2)
            weight[choice((0, 1))] *= choice((1, -1))
            weight_fun = weight[0]*x + weight[1]
            gram = sp.Matrix(
                [[sp.integrate(basis[i] * basis[j] * weight_fun, (x, lower_limit, upper_limit)) for j in range(3)] for i
                 in range(3)])
            if all(gram):
                minors = [gram[:k,:k].det() for k in range(1, gram.shape[0] + 1)]
                if any(m > 0 for m in minors) and any(m < 0 for m in minors):
                    gram_denoms = sp.lcm_list([a.as_numer_denom()[1] for a in gram]) / sp.gcd_list(
                        it.chain(weight, gram))
                    if all(abs(a * gram_denoms) < 100 for a in gram):
                        flag = True
        weight_fun *= gram_denoms
        # gram = sp.Matrix(
        #     [[sp.integrate(basis[i] * basis[j] * weight_fun, (x, lower_limit, upper_limit)) for j in range(3)] for i in
        #      range(3)])
        return lower_limit, upper_limit, (weight[0] * gram_denoms, weight[1] * gram_denoms)


class QuadFormDiagPolynomialsValues(Problem):
    def __init__(self):
        self.points, self.weights = self.generate()

    def render(self):
        weight_strs = []
        for i, w in enumerate(self.weights):
            if w > 0:
                weight_str = '{}{}'.format('+' if i else '', w if w > 1 else '')
            else:
                weight_str = '{}'.format(w if w < -1 else '-')
            weight_strs.append(weight_str)
        return 'На пространстве многочленов $\\mathbb{{R}}[x]_{{\\leqslant2}}$ многочленов степени не выше $2$ ' \
               'задана такая симметричная билинейная форма $B$, что соответствующая квадратичная форма $Q$ ' \
               'описывается формулой\n' \
               '\[ Q(f) = {}. \]\n' \
               'Диагонализируйте форму $B$ и предъявите соответствующий базис из многочленов.'.format(
            ' '.join('{}f({})^2'.format(weight_str, a) for a, weight_str in zip(self.points, weight_strs))
        )

    @staticmethod
    def generate():
        num_points = 4
        points_range = list(range(-3, 4))
        weights_range = list(it.chain(range(-3, 0), range(1, 4)))
        x = sp.symbols('x')
        basis = [sp.Poly(1, x), sp.Poly(x), sp.Poly(x ** 2)]
        flag = False
        while not flag:
            points = tuple(sorted(sample(points_range, k=num_points)))
            weights = tuple(choices(weights_range, k=num_points))
            gram = sp.Matrix(
                [[sum(w * basis[i].eval(a) * basis[j].eval(a) for a, w in zip(points, weights)) for j in range(3)] for i
                 in range(3)])
            if all(1 < abs(x) < 100 for x in gram):
                minors = [gram[:k,:k].det() for k in range(1, len(basis) + 1)]
                if any(m > 0 for m in minors) and any(m < 0 for m in minors) and all(m != 0 for m in minors):
                    flag = True
        return points, weights


class QuadFormOrthogonalDiagonalization(Problem):
    def __init__(self):
        self.form = self.generate()

    def render(self):
        variables = 'xyzw'
        form_str = ''
        for i in range(len(variables)):
            for j in range(i, len(variables)):
                form_str += '{}{}{}'.format('+' if self.form[i, j] > 0 and (i, j) != (0, 0) else '',
                                            self.form[i, j] * (2 if i != j else 1),
                                            '{}^2'.format(variables[i]) if i == j else '{}{}'.format(variables[i],
                                                                                                     variables[j]))
        return 'Привести квадратичную форму\n\\[ Q({}) = {} \\]\n' \
               'к главным осям при помощи ортогонального преобразования. ' \
               'Выразить $Q$ как линейную комбинацию квадратов линейных функций от тех же переменных.'.format(
            ','.join(variables), form_str
        )
        # return 'Diagonalize the quadratic form\n\\[ Q({}) = {} \\]\n' \
        #        'by an orthogonal transformation. ' \
        #        'Express $Q$ as the linear combination of squares of some linear functions of the original ' \
        #        'variables. Describe the shape of a surface given by $Q(x,y,z) = 1$.'.format(
        #     ','.join(variables), form_str
        # )

    @staticmethod
    def generate():
        flag = False
        size = 4
        while not flag:
            skewsym = sp.Matrix(size, size, lambda i, j: randint(-4, 5) if i < j else 0)
            skewsym -= skewsym.transpose()
            orth = skewsym2orth(skewsym)
            orth_denom = sp.lcm_list([x.as_numer_denom()[1] for x in orth])
            if orth_denom > 3:
                l1 = randint(1, 5)
                diag = sp.diag(l1, l1, randint(-5, -1), randint(-5, -1))
                a = orth.transpose() * diag * orth
                a_denom = sp.lcm_list([x.as_numer_denom()[1] for x in a])
                diag = a_denom * diag
                a = orth.transpose() * diag * orth
                flag = all(0 < abs(x) < 200 for x in a) and (a[0,0] > 0)
        return a
