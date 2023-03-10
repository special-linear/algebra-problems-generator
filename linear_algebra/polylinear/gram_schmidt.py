import numpy as np
from random import choice, randint

from linear_algebra.common import *

from problem import Problem

class GramSchmidt(Problem):
    def __init__(self, parameters):
        self.gram_matrix, self.vectors = self.gen_gram_schmidt(*parameters)

    def render(self):
        return 'На векторном пространстве $V=\mathbb{{R}}^4$ задано скаларное произведение, ' \
               'матрица Грама которого по отношению к стандартному базису имеет вид\n' \
               '\[ {}. \]\n' \
               'Найти ортогональный базис для подпространства, порожденного векторами\n' \
               '\[ {}. \]'.format(matrix_to_tex(self.gram_matrix), ',\ \n'.join(map(matrix_to_tex, self.vectors)))

    @staticmethod
    def gen_gram_schmidt(dim, entries_lim = 3):
        basis_change = np.identity(dim, dtype=int)
        gram_matrix = np.transpose(basis_change)*basis_change
        flag = True
        while flag:
            basis = gen_glnz_matrix(dim, entries_lim)
            vectors = [basis[:, i] for i in range(3)]
            flag = any([(np.transpose(u)*gram_matrix*v)[0, 0] == 0 for u in vectors for v in vectors])
        vectors.insert(2, choice([-1,1,2])*vectors[0]+choice([-2,-1,1])*vectors[1])
        return gram_matrix, tuple(vectors)