from problem import Problem
from linear_algebra.common import *
from random import choice, randint, choices, sample
import itertools as it
import sympy as sp
import math

class OrthogonalApproximateProducts(Problem):
    def __init__(self):
        self.phi_angle, self.phi_axis_letter, self.psi_angle, self.psi_axis, self.sigma_plane_letters, self.tau_plane_normal = self.gen_orthogonal_approx_products()

    def render(self):
        return 'Рассмотрим следующие ортогональные преобразования в $\\mathbb{{R}}^3$:\n' \
               '\\begin{{itemize}}\n' \
               '\\item $\\varphi$ --- поворот на ${}^\\circ$ вокруг координатной оси ${}$;\n' \
               '\\item $\\psi$ --- поворот на ${}^\\circ$ вокруг оси $\\langle{}^\\intercal\\rangle$;\n' \
               '\\item $\\sigma$ --- отражение относительно координатной плоскости ${}$;\n' \
               '\\item $\\tau$ --- отражение относительно плоскости, ортогональной вектору ${}^\\intercal$.\n' \
               '\\end{{itemize}}\n' \
               'Вычисляя приближенно, выпишите матрицы поворотов $\\varphi\\psi$ и $\\sigma\\tau$ ' \
               'в стандартном базисе и найдите для каждого из них ось вращения и угол поворота.\n' \
               'Для $\\varphi$ и $\\psi$ направление поворота против часовой стрелки, если вектор ' \
               'оси вращения направлен на наблюдателя.'.format(
            self.phi_angle, self.phi_axis_letter, self.psi_angle, self.psi_axis, ''.join(self.sigma_plane_letters),
            self.tau_plane_normal
        )
        # return 'Consider the following orthogonal transformations in $\\mathbb{{R}}^3$:\n' \
        #        '\\begin{{itemize}}\n' \
        #        '\\item $\\varphi$ --- a rotation by ${}^\\circ$ around the ${}$ coordinate axis;\n' \
        #        '\\item $\\psi$ --- a rotation by ${}^\\circ$ around $\\langle{}^\\intercal\\rangle$;\n' \
        #        '\\item $\\sigma$ --- a reflection through the coordinate plane ${}$;\n' \
        #        '\\item $\\tau$ --- a reflection through the plane orthogonal to ${}^\\intercal$.\n' \
        #        '\\end{{itemize}}\n' \
        #        'Calculating approximately, write down the matrices of rotations $\\varphi\\psi$ и $\\sigma\\tau$ ' \
        #        'in the standard basis and for each find the axis of rotation and the corresponding angle.\n' \
        #        'For $\\varphi$ and $\\psi$ the direction of rotations is counter-clockwise, if the rotation axis ' \
        #        'vector is pointing towards the observer.'.format(
        #     self.phi_angle, self.phi_axis_letter, self.psi_angle, self.psi_axis, ''.join(self.sigma_plane_letters),
        #     self.tau_plane_normal
        # )

    @staticmethod
    def gen_orthogonal_approx_products():
        phi_axis_letter = choice('xyz')
        phi_axis = sp.Matrix({'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}[phi_axis_letter])
        phi_angle = 5 * randint(4, 27)
        entries_vals = list(it.chain(*[[i, -i] for i in range(1, 6)]))
        flag = False
        while not flag:
            psi_axis = sp.Matrix(choices(entries_vals, k=3))
            phi_psi_dotprod = bil(phi_axis, psi_axis) / math.sqrt(bil(phi_axis, phi_axis) * bil(psi_axis, psi_axis))
            phi_psi_angle = math.degrees(math.acos(phi_psi_dotprod))
            if 20 <= phi_psi_angle <= 70 or 110 <= phi_psi_angle <= 160:
                flag = True
        psi_angle = phi_angle
        while abs(psi_angle - phi_angle) <= 30:
            psi_angle = 5 * randint(4, 27)
        sigma_plane_letters = tuple(sorted(sample('xyz', k=2)))
        tau_plane_normal = tuple(choices(entries_vals, k=3))
        return phi_angle, phi_axis_letter, psi_angle, tuple(psi_axis), sigma_plane_letters, tau_plane_normal
