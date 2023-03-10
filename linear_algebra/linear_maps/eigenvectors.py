from problem import Problem
from linear_algebra.common import *
import numpy as np
from random import choice
import itertools


class Eigenvectors(Problem):
    def __init__(self):
        self.matrix = self.gen_eigenvectors()

    def render(self):
        return 'Найти все собственные числа и собственные векторы оператора, заданного матрицей\n' \
               '\[ {}. \]'.format(matrix_to_tex(self.matrix))

    @staticmethod
    def gen_eigenvectors(entries_lim = 2):
        d = np.matrix(np.diag([0,0,1,1]))
        m = np.matrix(np.zeros((4, 4)), dtype=int)
        while 0 in list(itertools.chain.from_iterable(m.tolist())):
            c = gen_glnz_matrix(4, entries_lim)
            ci = np.rint(np.linalg.inv(c)).astype(int)
            m =c*d*ci
        return m
