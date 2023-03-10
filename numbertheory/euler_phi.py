from problem import Problem
import sympy as sp
from random import randint, sample, shuffle


class EulerPhi(Problem):
    def __init__(self):
        self.x = self.gen_x()

    def render(self):
        return 'Вычислите значение функции Эйлера $\\varphi({})$.'.format(self.x)

    @staticmethod
    def gen_x():
        x = 1
        pows = [1, 2, 3, 4]
        shuffle(pows)
        for i, nth in enumerate(sample(range(1, 5), k=3)):
            x *= sp.prime(nth)**pows[i]
        return x
