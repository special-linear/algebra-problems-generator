from problem import Problem
from linear_algebra.common import *


class SumIntersection3(Problem):
    def __init__(self, parameters):
        self.total_dim, self.U, self.V, self.W_eqs = self.gen_sum_intersection3(*parameters)

    def render(self):
        return "В пространстве $\mathbb{{R}}^{{{}}}$ рассматриваются три подпространства $U$, $V$, $W$:\n" \
               "\\begin{{gather*}}\n" \
               "U=\left\langle {} \\right\\rangle, \quad\n" \
               "V=\left\\{{ \\begin{{pmatrix}} {} \end{{pmatrix}} \\ \middle| \\ x,y,z\in\mathbb{{R}} \\right\\}}, \\\\\n" \
               "W=\\{{ v \\ \mid \\ Av=0 \\}},\quad \\text{{где}} \quad A = {}." \
               "\end{{gather*}}\n" \
               "Найти базис подпространства $(U+V)\cap W$.".format(
            self.total_dim,
            ',\ '.join(map(matrix_to_tex, [self.U.col(i) for i in range(self.U.shape[1])])),
            self.format_V(),
            matrix_to_tex(self.W_eqs)
        )

    @staticmethod
    def gen_sum_intersection3(n, entries_lim):
        dim_V, dim_UpV, dim_W = 0, 0, 0
        while dim_V != 3 or dim_UpV != 4 or dim_W != 3:
            U = sp.Matrix([[0 if j<i else choice((-1, 1))*randint(1, entries_lim) for j in range(0, 3)] for i in range(n)], dtype=int)
            V = sp.Matrix([[0 if (j<i-2 or i>3) else choice((-1, 1))*randint(1, entries_lim) for j in range(0, 3)] for i in range(n)], dtype=int)
            dim_V = len(V.columnspace())
            UpV = sp.transpose(sp.Matrix(list(map(sp.transpose, [U, V]))))
            dim_UpV = len(UpV.columnspace())
            W = sp.Matrix([[0 if (j<i-3 or i>4) else choice((-1, 1))*randint(1, entries_lim) for j in range(0, 3)] for i in range(n)], dtype=int)
            dim_W = len(W.columnspace())
        C = gen_glnz_matrix2(n, entries_lim=2)
        U, V, W = C*U, C*V, C*W
        W_eqs = sp.Matrix(list(map(sp.transpose, sp.transpose(W).nullspace())))
        C3 = gen_glnz_matrix2(n-3, entries_lim=2)
        W_eqs = C3*W_eqs
        W_eqs = W_eqs*sp.lcm([x.q for x in W_eqs])
        return n, U, V, W_eqs

    def format_V(self):
        rows = []
        for i in range(self.total_dim):
            summands = []
            for j in range(3):
                summand = '' if self.V[i, j] == 0 else ('{}{}'.format('' if self.V[i, j] < 0 or j == 0 else '+', self.V[i, j]))
                if summand:
                    summand += 'xyz'[j]
                summands.append(summand)
            row = ''.join(summands)
            if not row:
                row = '0'
            rows.append(row)
        return ' \\\\ '.join(rows)


class SumIntersectionZpZ(Problem):
    def __init__(self):
        self.u, self.v = self.gen_sum_intersection_zpz()

    def render(self):
        return "В пространстве столбцов высоты $6$ над полем $\mathbb{{F}}_5=\\{{ 0, \pm1, \pm2\\}}$" \
               " из пяти элементов найти базисы суммы и пересечения подпространств $U$ и $V$:\n" \
               "\[ U = \left\langle {} \\right\\rangle, \quad V = \left\langle {} \\right\\rangle. \]".format(
            ', '.join(matrix_to_tex(self.u.col(i)) for i in range(self.u.shape[1])).replace('4', '-1').replace('3', '-2'),
            ', '.join(matrix_to_tex(self.v.col(i)) for i in range(self.v.shape[1])).replace('4', '-1').replace('3', '-2')
        )
        # return "In the vector space of columns of height $6$ over the fields $\mathbb{{F}}_5=\\{{ 0, \pm1, \pm2\\}}$" \
        #        " with five elements find the bases for the sum and the intersection of the subspaces $U$ and $V$:\n" \
        #        "\[ U = \left\langle {} \\right\\rangle, \quad V = \left\langle {} \\right\\rangle. \]".format(
        #     ', '.join(matrix_to_tex(self.u.col(i)) for i in range(self.u.shape[1])).replace('4', '-1').replace('3',
        #                                                                                                        '-2'),
        #     ', '.join(matrix_to_tex(self.v.col(i)) for i in range(self.v.shape[1])).replace('4', '-1').replace('3',
        #                                                                                                        '-2')
        # )

    @staticmethod
    def gen_sum_intersection_zpz():
        u = sp.Matrix([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]])
        v = sp.Matrix([[1, 0, 0, 2],
                       [0, -1, 0, -1],
                       [1, 0, 0, -1],
                       [1, 2, 0, 2],
                       [0, 0, 1, -2],
                       [0, 0, 0, 0]])
        c = gen_glzmz_matrix2(6, modulo=5)
        mod5 = lambda x: x % 5
        return (c*u).applyfunc(mod5), (c*v).applyfunc(mod5)
