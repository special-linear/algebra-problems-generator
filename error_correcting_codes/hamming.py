from problem import Problem
from random import randint, choice
import itertools as it
import sympy as sp


class HammingCodeWords(Problem):
    def __init__(self):
        self.messages = self.generate()

    def render(self):
        return 'Рассмотрим код Хэмминга длины $7$. Для каждого из следующих элементов пространства ' \
               'принимаемых сообщений определите, является ли оно кодовым словом. Для тех, которые не являются, ' \
               'найдите ближайшее кодовое слово.\n\\[ {} \\]'.format(
            ' \\qquad '.join('\\mathtt{{{}}}'.format(''.join(map(str, m))) for m in self.messages)
        )

    @staticmethod
    def generate():
        num_messages = 3
        F = sp.FiniteField(2)
        f = (F(0), F(1))
        h = sp.Matrix(list(filter(any, it.product(f, repeat=3)))).transpose()
        messages = set()
        while len(messages) < num_messages:
            m = sp.ImmutableMatrix(7, 1, lambda i, _: choice(f))
            if any(m) and not any(map(F, h * m)):
                messages.add(m)
        messages = list(map(list, messages))
        for i in range(1, num_messages):
            j = randint(0, 6)
            messages[i][j] = (messages[i][j] + 1) % 2
        return tuple(map(tuple, messages))
