from problem import Problem
from random import randint, choice, sample, shuffle


class TrigMultAngle(Problem):
    def __init__(self):
        self.fs = self.gen_trig_mult_angle()

    @staticmethod
    def gen_trig_mult_angle():
        functions = sample(['\cos', '\cos', '\sin', '\sin'], 4)
        powers = sample([1, 2, 2, 3], 4)
        arguments = sample(['\\frac{x}{2}', '\\frac{x}{3}', '\\frac{3x}{2}', '\\frac{2x}{3}',
                            '\\frac{x}{4}', '\\frac{3x}{4}', '2x', '3x'], 4)
        return list(zip(functions, powers, arguments))

    @staticmethod
    def display_trig(f, p, a):
        return '{}{}\left({}\\right)'.format(f, '^{{{}}}'.format(p) if p > 1 else '', a)

    def render(self):
        return 'Представить в виде линейной комбинации синусов и косинусов кратных углов ' \
               '(коэффициенты кратности не обязательно целые):\n' \
               '\[ \left( {} - {} \\right) \cdot \left( {} + {} \\right). \]'.format(
            *map(lambda x: self.display_trig(*x), self.fs)
        )
        # return 'Rewrite as the linear combination of sines and cosines of multiples of $x$ ' \
        #        '(the multiplicity coefficients are not necessarily integer):\n' \
        #        '\[ \left( {} - {} \\right) \cdot \left( {} + {} \\right). \]'.format(
        #     *map(lambda x: self.display_trig(*x), self.fs)
        # )
