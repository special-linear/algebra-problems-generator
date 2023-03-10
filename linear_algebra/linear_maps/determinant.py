from numbertheory.polynomial import Polynomial
from linear_algebra.common import *
import random
import itertools as it
import sympy as sp
from os.path import abspath, relpath, join, dirname

from problem import Problem
from list_problem import FromListProblem

class Determinant(Problem):
    def __init__(self, parameters):
        self.matrix = self.gen_determinant(*parameters)

    def render(self):
        return 'Вычислить определитель матрицы над кольцом $\mathbb{{F}}_3[t]$:\n' \
               '\[ {}. \]'.format(matrix_to_tex(self.matrix))
        # return 'Calculate the determinant of the following matrix over the ring $\mathbb{{F}}_3[t]$:\n' \
        #        '\[ {}. \]'.format(matrix_to_tex(self.matrix))

    @staticmethod
    def gen_determinant(dim):
        m = gen_glzmz_matrix(dim, 3).tolist()
        for i, j in random.sample(list(it.product(range(dim), repeat=2)), int(1.5 * dim)):
            m[i][j] += Polynomial([random.choice([0, 0, 0, 0, 1, 2]), random.choice([1, 2]), 0])
        return np.matrix(m)


class DeterminantPolynomial(Problem):
    def __init__(self, parameters):
        self.matrix = self.gen_determinant(*parameters)

    def render(self):
        return 'Вычислить определитель матрицы\n\[ {}. \]'.format(matrix_to_tex(self.matrix))

    @staticmethod
    def gen_determinant(dim):
        t = sp.symbols('t')
        c = gen_glnz_matrix(dim, 2)
        m = sp.eye(dim)
        for i in range(3):
            m[i,i] = sp.poly(t+1)
        cm = np.matrix(c*m*np.invert(c))
        for i,j in it.product(range(dim), repeat=2):
            cm[i,j] = Polynomial(cm[i,j].coeffs())
        return cm



class DeterminantTheory(FromListProblem):
    problems = [
        'Доказать, что определитель матрицы \\[\\begin{pmatrix} A & A^2 \\\\ A^2 & A^2 \end{pmatrix},\\]'
        ' где $A$ --- произвольная квадратная матрица, равен $0$.',
        'Доказать, что \\[\det\\begin{pmatrix} E_m & B \\\\ C & D \end{pmatrix} = \det(D-CB),\\]'
        ' если $B$ и $C$ --- произвольные $m{\\times}n$- и $n{\\times}m$-матрицы, а $D$ ---'
        ' квадратная матрица порядка $n$.',
        'Доказать, что \\[\det(E_m+AB)=\det(E_n+BA),\] если $A$ --- произвольная $m{\\times}n$-матрица,'
        ' а $B$ --- произвольная $n{\\times}m$-матрица.',
        'Доказать, что если матрицы $A$ и $B$ коммутируют, то'
        ' \\[\det\\begin{pmatrix} A & B \\\\ C & D \end{pmatrix} = \det(DA-CB).\\]',
        'Для квадратных матриц $A$ и $B$ порядков $m$ и $n$ обозначим через $A\otimes B$ матрицу порядка $mn$,'
        ' составленную из блоков $a_{ij}B$, где $A=(a_{ij})$. Вычислить $\det(A\otimes B)$.',
        'Доказать, что \\[ \det\\begin{pmatrix} A & B \\\\ B & A \end{pmatrix} = \det(A+B) \det(A-B),\\]'
        ' если $A$ и $B$ --- квадратные матрицы одного размера.',
        'Доказать, что \\[ \det\\begin{pmatrix} 0 & A \\\\ B & 0 \end{pmatrix} = \det(A)\det(B), \]'
        ' если $A$ и $B$ --- квадратные матрицы одного размера.'
    ]


class DeterminantParametricBasic(FromListProblem):
    problems_source = (join(dirname(__file__), 'determinant.toml'), 'determinant_parametric_basic')

    def render(self):
        return 'Вычислить определитель\n\\[ \\begin{{vmatrix}} {} \\end{{vmatrix}}. \\]'.format(self.text)


class DeterminantParametricCombinatorial(FromListProblem):
    problems_source = (join(dirname(__file__), 'determinant.toml'), 'determinant_parametric_combinatorial')

    def render(self):
        return 'Вычислить определитель\n\\[ \\begin{{vmatrix}} {} \\end{{vmatrix}}. \\]'.format(self.text)
