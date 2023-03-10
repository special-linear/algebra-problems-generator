import numpy as np
import sympy as sp
from random import randint, choice, sample
from math import floor
import itertools as it


def gen_glnz_matrix(n, entries_lim = 3):
    flag = False
    while not flag:
        m = np.matrix([[choice((1, -1))*randint(1, entries_lim) for _ in range(n)] for __ in range(n)], dtype=int)
        flag = np.linalg.det(m) in (1, -1)
    return m


def gen_glnz_matrix2(n, entries_lim = 3):
    flag = False
    while not flag:
        m = sp.Matrix([[choice((1, -1))*randint(1, entries_lim) for _ in range(n)] for __ in range(n)], dtype=int)
        flag = sp.det(m) in (1, -1)
    return m


def gen_dense_glnz_matrix(n, entries_lim = 3):
    a = sp.zeros(n)
    while not all(x != 0 for x in a):
        a = gen_glnz_matrix2(n, entries_lim=entries_lim)
    return a


def gen_sparse_glnz_matrix(n, entries_lim=3, sparsity=0.5):
    flag = False
    positions = list(it.product(range(n), repeat=2))
    k = floor(n**2 * sparsity)
    while not flag:
        m = sp.zeros(n)
        nonzero_entries = sample(positions, k=k)
        for i, j in nonzero_entries:
            m[i,j] = choice((1, -1))*randint(1, entries_lim)
        flag = sp.det(m) in (1, -1)
    return m


def gen_sparse_glnq_matrix(n, entries_lim=3, sparsity=0.5):
    flag = False
    positions = list(it.product(range(n), repeat=2))
    k = floor(n**2 * sparsity)
    while not flag:
        m = sp.zeros(n)
        nonzero_entries = sample(positions, k=k)
        for i, j in nonzero_entries:
            m[i,j] = choice((1, -1))*randint(1, entries_lim)
        flag = sp.det(m) != 0
    return m


def gen_glzmz_matrix(n, modulo = 3):
    flag = False
    zmz = list(it.chain([0], range(1, modulo), range(1, modulo)))
    good_dets = list(range(1, modulo))
    while not flag:
        m = np.matrix([[choice(zmz) for _ in range(n)] for __ in range(n)], dtype=int)
        flag = (np.linalg.det(m) % modulo) in good_dets
    return m


def gen_glzmz_matrix2(n, modulo = 3):
    flag = False
    zmz = list(it.chain([0], range(1, modulo), range(1, modulo)))
    good_dets = list(range(1, modulo))
    while not flag:
        m = sp.Matrix([[choice(zmz) for _ in range(n)] for __ in range(n)], dtype=int)
        flag = (sp.det(m) % modulo) in good_dets
    return m


def gen_row_echelon_matrix(m, n, pivots, entries_lim):
    rem = sp.zeros(m, n)
    for i, j0 in enumerate(pivots):
        rem[i, j0] = 1
        for j in range(j0 + 1, n ):
            if j not in pivots:
                rem[i, j] = randint(-entries_lim, entries_lim)
    return rem


def skewsym2orth(m):
    id_m = sp.eye(m.shape[0])
    return (m - id_m).inv() * (m + id_m)


def good_charpoly(m):
    n = m.shape[0]
    lamda = sp.symbols('lamda')
    chp = m.charpoly(lamda)
    values = list(it.chain(*[[i, -i] for i in range(1, 10)]))
    for r in values:
        if chp == sp.poly((lamda - r)**n):
            return r
    return False


def is_okay_charpoly(m):
    n = m.shape[0]
    lamda = sp.symbols('lamda')
    chp = m.charpoly(lamda)
    if chp == sp.poly((lamda - 1) ** 3 * (lamda - 2)) or chp == sp.poly(
            (lamda - 1) ** 3 * (lamda + 2)) or chp == sp.poly((lamda - 1) ** 3 * (lamda + 1)) or chp == sp.poly(
            (lamda - 1) ** 3 * (lamda + 3)) or chp == sp.poly((lamda - 1) ** 3 * (lamda - 3)):
        return 1
    elif chp == sp.poly((lamda + 1) ** 3 * (lamda - 2)) or chp == sp.poly(
            (lamda + 1) ** 3 * (lamda + 2)) or chp == sp.poly((lamda + 1) ** 3 * (lamda - 1)) or chp == sp.poly(
            (lamda + 1) ** 3 * (lamda - 3)) or chp == sp.poly((lamda + 1) ** 3 * (lamda + 3)):
        return -1
    elif chp == sp.poly((lamda - 2) ** 3 * (lamda - 1)) or chp == sp.poly(
            (lamda - 2) ** 3 * (lamda + 1)) or chp == sp.poly((lamda - 2) ** 3 * (lamda + 2)) or chp == sp.poly(
            (lamda - 2) ** 3 * (lamda - 3)) or chp == sp.poly((lamda - 2) ** 3 * (lamda + 3)):
        return 2
    elif chp == sp.poly((lamda + 2) ** 3 * (lamda - 1)) or chp == sp.poly(
            (lamda + 2) ** 3 * (lamda + 1)) or chp == sp.poly((lamda + 2) ** 3 * (lamda - 2)) or chp == sp.poly(
        (lamda + 2) ** 3 * (lamda - 3)) or chp == sp.poly((lamda + 2) ** 3 * (lamda + 3)):
        return -2
    else:
        return False


def bil(u, v):
    return (u.transpose()*v)[0,0]


def sp_vector2tuple(v):
    return tuple(map(lambda x: (x,), v))


def vector2tex(v):
    return '\\begin{{pmatrix}} {} \\end{{pmatrix}}'.format(' \\\\ '.join(map(str, v)))


def matrix_to_tex(m, print_zeroes=True):
    if print_zeroes:
        return '\\begin{{pmatrix}} {} \\end{{pmatrix}}'.format(' \\\\ '.join(' & '.join(map(str, row)) for row in m.tolist()))
    else:
        return '\\begin{{pmatrix}} {} \\end{{pmatrix}}'.format(' \\\\ '.join(' & '.join(map(lambda ie: str(ie[1]) if ie[1] or i == ie[0] else '', enumerate(row))) for i, row in enumerate(m.tolist())))


def linear_system_tex(a, b, vars):
    return '\\begin{{cases}} {} \\end{{cases}}'.format(
        ' \\\\ '.join('{} = {}'.format(' '.join('{}{}{}'.format('+' if i != 0 and c > 0 else '', c if abs(c) > 1 else '-' if c == -1 else '', x) if c else '' for i, c, x in zip(it.count(), row, vars)), bi) for row, bi in zip(a, b))
    )
