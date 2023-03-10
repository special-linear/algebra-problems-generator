from problem import Problem
from random import randint, choice, shuffle


class ExteriorPowerExpansion(Problem):
    def __init__(self):
        self.dimension, self.vectors = self.gen_exterior_power_expansion()

    def render(self):
        return 'Пусть $V$ --- векторное пространство с базисом $e_1,\\ldots,e_{{{}}}$. Выразить\n\\[ {} \\]\n' \
               'в стандартном базис $\\wedge^3V$.'.format(
            self.dimension,
            ' \\wedge '.join('\\big( {} \\big)'.format(self.vector_as_sum_tex(v)) for v in self.vectors)
        )
        # return 'Let $V$ be a vector space with a basis $e_1,\\ldots,e_{{{}}}$. Express\n\\[ {} \\]\n' \
        #        'in the standard basis of $\\wedge^{{{}}}V$.'.format(
        #     self.dimension,
        #     ' \\wedge '.join('\\big( {} \\big)'.format(self.vector_as_sum_tex(v)) for v in self.vectors),
        #     len(self.vectors)
        # )

    @staticmethod
    def gen_exterior_power_expansion():
        num_vectors = 3
        dimension = 4
        support_size = 2
        coeff_lim = 3
        vectors = set()
        while not all(any(v[i] for v in vectors) for i in range(dimension)):
            vectors = set()
            while len(vectors) < num_vectors:
                v = [choice((1, -1)) * randint(1, coeff_lim) for j in range(support_size)] \
                    + [0] * (dimension - support_size)
                shuffle(v)
                v = tuple(v)
                vectors.add(v)
        return dimension, list(vectors)

    @staticmethod
    def vector_as_sum_tex(v):
        res = ''
        for i, vi in enumerate(v):
            if vi:
                res += '{}{}e_{{{}}}'.format('+' if vi > 0 else '-' if vi == -1 else '', '' if vi in (1, -1) else vi, i+1)
        return res.lstrip('+')
