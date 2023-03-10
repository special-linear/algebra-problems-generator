from problem import Problem
import sympy as sp
from linear_algebra.common import good_charpoly, matrix_to_tex, gen_glnz_matrix2, gen_dense_glnz_matrix
from random import sample, choices, choice, randint
import itertools as it


def matrix_has_good_jf(a):
    n = a.shape[0]
    r = good_charpoly(a)
    if r and all(abs(x) < 100 for x in sp.flatten(a)):
        b = a - r * sp.eye(n)
        bp = b
        d_prev = n
        d_new = b.rank()
        ds = []
        while d_prev != d_new:
            ds.append(d_prev)
            d_prev = d_new
            bp *= b
            d_new = bp.rank()
        ds.extend([0, 0])
        blocks_sizes = tuple(ds[i] - 2 * ds[i - 1] + ds[i - 2] for i in range(2, len(ds)))
        return blocks_sizes in [(0, 1, 1), (2, 0, 1), (1, 2), (0, 1, 0, 1), (1, 1, 1)]
    else:
        return False


class JordanFormMatrix(Problem):
    def __init__(self):
        self.matrix = self.gen_jordan_form()

    def render(self):
        return 'Найти жорданову форму и соответствующий жорданов базис матрицы\n\\[ {}. \\]'.format(
            matrix_to_tex(self.matrix)
        )

    @staticmethod
    def gen_jordan_form():
        blocks = [(2, 3), (2, 1), (-1, 2)]
        c_diag_block_sizes = [2, 3, 1]
        n = sum(size for eigval, size in blocks)
        jordan_matrix = sp.diag(*[sp.jordan_cell(*b) for b in blocks])
        a = sp.zeros(n)
        a_nonzero_pos = []
        for i, cbs in enumerate(c_diag_block_sizes):
            a_nonzero_pos.append((sum(c_diag_block_sizes[:i+1]) - 1, sum(c_diag_block_sizes[:i])))
        while any(abs(x) >= 10 for x in a) or any(a[i,j] == 0 for i, j in a_nonzero_pos):
            c = sp.diag(*[gen_glnz_matrix2(size) for size in c_diag_block_sizes])
            for i, j in it.combinations(range(n), r=2):
                if c[i,j] == 0:
                    c[i,j] = randint(-2, 2)
            a = c * jordan_matrix * c.inv()
        return a


dim = 6


class JordanFormPolynomial(Problem):
    def __init__(self):
        self.phi = self.gen_jordan_form(dim)

    def render(self):
        return 'На векторном пространстве $V = \mathbb{{C}}[t]_{{\leqslant {}}}$ многочленов степени не выше ${}$ ' \
               'действует линейный оператор $\\varphi$, заданный формулой\n' \
               '\[ \\varphi\colon f \longmapsto {}. \]\n' \
               'Найти жорданову форму форму и жорданов базис для $\\varphi$ (элементы базиса --- многочлены).'.format(
            dim-1, dim-1, self.phi
        )

    @staticmethod
    def gen_jordan_form(n):
        flag = True
        while flag:
            num_summands = 3
            indices = list(range(len(fs_ext_keys)))
            ii = [fs_ext_keys[i] for i in sample(indices, num_summands)]
            cs = [1] + choices([3, 2, 1, -1, -2, -3], k=num_summands-1)
            a = sum([cs[num] * fs_ext[i] for num, i in enumerate(ii)], sp.zeros(n))
            flag = not matrix_has_good_jf(a)
        res = ''.join(
            ('+' if c > 0 else '-') + (str(c) if c > 1 else str(abs(c)) if c < -1 else '') + f for c, f in zip(cs, ii))
        return res[1:] if res[0] == '+' else res


n = dim - 1


def pad_zeroes(l, n):
    return [0] * (n + 1 - len(l)) + l


def to_basis(f):
    return list(reversed(pad_zeroes(f.all_coeffs(), n)))


def phi_matrix(phi):
    return sp.Matrix([to_basis(phi(f)) for f in basis]).transpose()


t = sp.symbols('t')
basis = [0 * sp.poly(t) + 1] + [sp.poly(t ** k) for k in range(1, n + 1)]

fs_ext = dict()
fs_ext['f'] = sp.eye(n + 1)
fs_ext["f'"] = phi_matrix(lambda f: sp.diff(f, t))
fs_ext["f''"] = phi_matrix(lambda f: sp.diff(f, t, t))
fs_ext["f'''"] = phi_matrix(lambda f: sp.diff(f, t, t, t))
# fs_ext["tf'"] = phi_matrix(lambda f: t*sp.diff(f, t))
# fs_ext["tf''"] = phi_matrix(lambda f: t*sp.diff(f, t, t))
# fs_ext["t^2f''"] = phi_matrix(lambda f: t**2*sp.diff(f, t, t))
# fs_ext["tf'''"] = phi_matrix(lambda f: t*sp.diff(f, t, t, t))
# fs_ext["t^2f'''"] = phi_matrix(lambda f: t**2*sp.diff(f, t, t, t))
fs_int = dict()
for alpha, beta in it.product([2, 1, -1, -2], [2, 1, 0, -1, -2]):
    if (alpha, beta) != (1, 0):
        fs_int['{}{{}}{}'.format(alpha if abs(alpha) != 1 else '-' if alpha == -1 else '',
                                 '+' + str(beta) if beta > 0 else '-' + str(
                                     abs(beta)) if beta < 0 else '')] = phi_matrix(
            lambda f: sp.poly(f.subs(t, alpha * t + beta), t))
for f_e, f_i in it.product(fs_ext.keys(), fs_int.keys()):
    fs_ext['{}({})'.format(f_e, f_i.format('t'))] = fs_ext[f_e]*fs_int[f_i]
for k, alpha in it.product(range(1, n), range(-2, 3)):
    pass
    # fs_ext['t^{}f({})'.format(k, alpha)] = phi_matrix(lambda f: sp.poly(t**k*f.subs(t, alpha), t))
    # fs_ext["t^{}f'({})".format(k, alpha)] = phi_matrix(lambda f: sp.poly(t ** k * sp.diff(f, t).subs(t, alpha), t))
fs_ext_keys = list(fs_ext.keys())


class JordanFormSymmMat(Problem):
    def __init__(self):
        self.mat = self.gen_jordan_form()

    def render(self):
        return 'На векторном пространстве $V = \\{{ X\in M(3,\\mathbb{{C}}) \mid X=X^\\top \\}}$ ' \
               'симметричных матриц $3{{\\times}}3$ действует ' \
               'линейный оператор $\\varphi$, заданный формулой\n' \
               '\[ \\varphi\colon X \longmapsto Y\\cdot X\\cdot Y^\\top,\quad\\text{{где}}\\quad Y = {}. \]\n' \
               'Найти жорданову форму форму и жорданов базис для $\\varphi$ (элементы базиса --- матрицы).'.format(
            matrix_to_tex(self.mat)
        )
        # return 'On the vector space $V = \{{ X\in M(3,\mathbb{{C}}) \mid X=X^\\top \}}$ ' \
        #        'acts a linear operator $\\varphi$ given by the formula\n' \
        #        '\[ \\varphi\colon X \longmapsto Y\cdot X\cdot Y^\intercal,\quad\\text{{where}}\quad Y = {}. \]\n' \
        #        'Find the Jordan normal form and the Jordan basis for $\\varphi$ ' \
        #        '(note that the elements of the basis are $3{{\\times}}3$ symmetric matrices).'.format(
        #     matrix_to_tex(self.mat)
        # )

    @staticmethod
    def gen_jordan_form():
        indices = list(it.combinations_with_replacement(range(3), r=2))
        es = [sp.Matrix(3, 3, lambda i, j: 1 if (i, j) in ((p, q), (q, p)) else 0) for p, q in indices]
        flag = True
        while flag:
            y = sp.Matrix(3, 3,
                          lambda i, j: 0 if i > j else -1 if i == j else choice((-1,1))*randint(2, 5))
            y[choice(((0, 1), (0, 2), (1, 2)))] = 0
            yesyt = [y*e*y.transpose() for e in es]
            a = sp.Matrix(len(indices), len(indices), lambda i, j: yesyt[j][indices[i]])
            if all(any(a[i,j] for i in range(j)) for j in range(1, len(indices))):
                flag = not matrix_has_good_jf(a)
        return y


class JordanFormMatMul(Problem):
    def __init__(self):
        self.y = self.gen_jordan_form()

    def render(self):
        return 'На векторном пространстве $M({},\\mathbb{{R}})$ задан оператор $\\varphi$, действующие по правилу\n' \
               '\\[ \\varphi(X) = X\\cdot {}. \\]\n' \
               'Найти жорданову форму форму и жорданов базис для $\\varphi$ (элементы базиса --- матрицы).'.format(
            2, matrix_to_tex(self.y)
        )

    @staticmethod
    def gen_jordan_form():
        dim = 2
        indices = list(it.product(range(dim), repeat=2))
        print(len(indices))
        es = [sp.Matrix(dim, dim, lambda i, j: 1 if (i, j) in ((p, q), (q, p)) else 0) for p, q in indices]
        flag = True
        while flag:
            y, z, u, v = (sp.Matrix(dim, dim, lambda i, j: randint(-5, 5)) for _ in range(4))
            eys = [y * e * z + u * e.transpose() * v for e in es]
            a = sp.Matrix(len(indices), len(indices), lambda i, j: eys[j][indices[i]])
            # print(sp.factor_list(a.charpoly(sp.symbols('x'))))
            flag = not matrix_has_good_jf(a)
        sp.pprint([y, z])
        sp.pprint(a)
        return y
