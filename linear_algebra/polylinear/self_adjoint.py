from problem import Problem
import sympy as sp
from random import randint, choice


class SelfAdjointExistence(Problem):
    def __init__(self):
        self.vectors = self.gen_vectors()

    def render(self):
        return 'Существует ли такой самосопряженный оператор $\\varphi$ на $\\mathbb{{R}}^3$, что\n' \
               '\\[ \\varphi({}^\\top) = {}^\\top, \\quad \\varphi({}^\\top) = {}^\\top? \\]\n' \
               'Можно ли дополнительно потребовать, чтобы\n' \
               '\\[ \\varphi({}^\\top) = {}^\\top? \\]\n' \
               'В обоих случаях если такой оператор существует, предъявите его, если нет, докажите это.'.format(
            *self.vectors
        )

    @staticmethod
    def gen_vectors():
        flag = False
        while not flag:
            a = sp.Matrix([[choice((1, -1)) * randint(1, 3) if j > i else 0 for j in range(3)] for i in range(3)])
            a = a + a.transpose() + sp.diag(*[choice((1, -1)) * randint(1, 3) for _ in range(3)])
            u, v, w = (sp.Matrix(3, 1, [choice((1, -1)) * randint(1, 3) for _ in range(3)]) for _ in range(3))
            au, av, aw = map(lambda x: a * x, [u, v, w])
            awp = aw + sp.Matrix(3, 1, [randint(-1, 1) for _ in range(3)])
            flag = all(all(abs(y) < 10 for y in x) for x in (au, av, awp)) \
                   and u.dot(av) == au.dot(v) and u.dot(awp) == au.dot(w) and v.dot(awp) != av.dot(w)
        return tuple(map(tuple, (u, au, v, av, w, awp)))
