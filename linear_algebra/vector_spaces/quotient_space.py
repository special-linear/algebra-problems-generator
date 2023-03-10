from problem import Problem
from random import randint, choice


class QuotientSpaceBasis(Problem):
    def __init__(self):
        self.points = self.gen_points()

    def render(self):
        return 'В пространстве $V = \\mathbb{{R}}[x]_{{\\leqslant 5}}$ рассмотрим подпространство\n' \
               '\\[ U = \\{{ f\\in\\mathbb{{R}}[x]_{{\leqslant 4}} \\mid f({})=f({})=0 \\}}. \\]\n' \
               'Найдите какой-нибудь базис $V/U$.'.format(
            *self.points
        )

    @staticmethod
    def gen_points():
        points = (0, 0)
        while points[0] == points[1]:
            points = tuple(choice((1, -1)) * randint(1, 4) for _ in range(2))
        return points

