from problem import Problem
from random import randint


class EuclideanDivision(Problem):
    def __init__(self):
        self.a, self.b = self.gen_euclidean_division()

    def render(self):
        return 'Поделите с остатком (указав неполное частное и остаток) ' \
               '${0}$ и $-{0}$ на ${1}$ и $-{1}$ (итого $4$ деления).'.format(
            self.a, self.b
        )

    @staticmethod
    def gen_euclidean_division():
        a, b, q, r = [0] * 4
        while not (r and abs(q) > 1):
            a = randint(41, 99)
            b = randint(11, 40)
            q, r = divmod(a, b)
        return a, b
