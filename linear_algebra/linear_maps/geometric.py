import os

import itertools
import more_itertools

from problem import Problem

from random import choice, sample, randint


def det(f1, f2, f3):
    res = f1[0] * f2[1] * f3[2] + f1[2] * f2[0] * f3[1] + f1[1] * f2[2] * f3[0]
    res += -f1[2] * f2[1] * f3[0] - f1[1] * f2[0] * f3[2] - f1[0] * f2[2] * f3[1]
    return res


class LinAlgGeometric(Problem):

    points_labels_pos = {
        # reflection points
        (0, 1, 0.5): 'above left',
        (0.5, 1, 1): 'above',
        (0.5, 1, 0): 'below',
        (1, 1, 0.5): 'below',
        (1, 0.5, 0): 'right',
        (1, 0, 0.5): 'below right',
        (1, 0.5, 1): 'right',
        # basis points
        (0, 1, 1): 'above',
        (1, 1, 0): 'below left',
        (1, 0, 1): 'right',
        (1, 1, 1): 'above right'
    }

    reflection_points = [(0, 1, 0.5), (0.5, 1, 1), (0.5, 1, 0), (1, 1, 0.5), (1, 0.5, 0), (1, 0, 0.5), (1, 0.5, 1)]

    points = list(itertools.chain(points_labels_pos.keys()))

    def __init__(self):
        self.reflection_point = choice(self.reflection_points)
        flag = False
        while not flag:
            f1, f2, f3 = sample(self.points, 3)
            flag = det(f1, f2, f3) != 0
        self.basis = (f1, f2, f3)
        flag = False
        while not flag:
            rc = [randint(-3, 3) for _ in range(9)]
            flag = (0 < rc.count(0) < 4) and (0 < rc.count(3)+rc.count(-3) < 3)
        self.matrix = tuple(map(tuple, more_itertools.chunked(rc, 3)))
        flag = False
        while not flag:
            f1, f2, f3 = sample(self.points, 3)
            flag = det(f1, f2, f3) != 0 and self.reflection_point not in (f1, f2, f3)
            intersection_count = 0
            for v in self.basis:
                if v in (f1, f2, f3):
                    intersection_count += 1
            flag = flag and intersection_count <= 1
        self.target_basis = (f1, f2, f3)

    def render(self):
        points_list = more_itertools.unique_everseen(itertools.chain(((1, 1, 1), self.reflection_point),
                                                                      self.basis, self.target_basis))
        points_letters = dict(zip(points_list, 'ABCDEFGH'))
        points_tikz = []
        points_labels_tikz = []
        for point, letter in points_letters.items():
            points_tikz.append('\\fill {} circle (0.05);'.format(str(point)))
            points_labels_tikz.append('\\node[{}] at {} {{\\large ${}$}};'.format(self.points_labels_pos[point],
                                                                          str(point), letter))
        basis_tex = '$\\{{ {} \\}}$'.format(', '.join(points_letters[v] for v in self.basis))
        matrix_tex = '\\begin{{pmatrix}} {} \\end{{pmatrix}}'.format('\\\\'.join('&'.join(map(str,row))
                                                                               for row in self.matrix))
        target_basis_tex = '$\\{{ {} \\}}$'.format(', '.join(points_letters[v] for v in self.target_basis))
        with open(os.path.dirname(__file__)+'/linalg_geometric_template.txt', encoding='utf-8', mode='r') as template_file:
            template = template_file.read().strip().replace(u'\ufeff', '')
            return template.format(points='\n'.join(points_tikz),
                                   points_labels='\n'.join(points_labels_tikz),
                                   reflection_point=points_letters[self.reflection_point],
                                   basis=basis_tex,
                                   matrix=matrix_tex,
                                   target_basis=target_basis_tex)

