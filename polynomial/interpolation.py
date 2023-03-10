from problem import Problem
from numbertheory.gaussint import GaussInt
from random import randint


class InterpolationGaussInt(Problem):
    def __init__(self):
        self.xs, self.vs = self.gen_interpolation_gaussint()

    def render(self):
        return 'Про многочлен $f\in\mathbb{{C}}[t]$ степени $\\leqslant 3$ известно, ' \
               'что он принимает значения, указанные в таблице\n' \
               '\[ \\begin{{array}}{{c|cccc}} x & {} \\\\\\hline f(x) & {}  \\end{{array}} \]\n' \
               'Вычислить старший коэффициент $f$ и значение $f$ в точке $0$.'.format(' & '.join(map(str, self.xs)),
                                                                        ' & '.join(map(str, self.vs)))
        # return 'The polynomial $f\in\mathbb{{C}}[t]$ of degree $\\leqslant 3$ ' \
        #        'takes the following values\n' \
        #        '\[ \\begin{{array}}{{c|cccc}} x & {} \\\\\\hline f(x) & {}  \\end{{array}} \]\n' \
        #        'Find the leading coefficient and the free term of $f$.'.format(' & '.join(map(str, self.xs)),
        #                                                                 ' & '.join(map(str, self.vs)))

    @staticmethod
    def gen_interpolation_gaussint():
        xs = [GaussInt(1, 0), GaussInt(0, 1), GaussInt(-1, 0), GaussInt(0, -1)]
        vs = [0]
        while not all(vs):
            f = [0, randint(-3, 4), randint(2, 4)]
            vs = [sum(f[i] * x ** i for i in range(3)) for x in xs]
        return xs, vs
