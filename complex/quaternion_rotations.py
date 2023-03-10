from list_problem import FromListProblem
from problem import Problem
from random import choice, shuffle
import itertools as it


class QuaternionRotationsHandcrafted(FromListProblem):
    problems = [
        ('1,1,\\sqrt 2', 120, '3,6,2', 90, '9,2,6'),
        ('2,\\sqrt 3,0', 60, '1,2,3', 120, '5,6,30'),
        ('-1,2,-\\sqrt 2', 120, '18,1,30', 120, '4,32,7'),
        ('\\sqrt 3,1,-1', 60, '16,8,2', 90, '3,22,6'),
        ('-1,\\sqrt 2,2', 90, '4,8,21', 60, '32,1,8'),
        ('3,-1,\\sqrt 3', 60, '4,8,1', 60, '28,17,4'),
        ('-\\sqrt 3,1,-2', 120, '2,7,6', 60, '8,4,8'),
        ('2,\\sqrt 2,-2', 90, '2,14,5', 120, '6,6,3'),
        ('1,\\sqrt 3,-3', 90, '12,3,24', 270, '3,4,12'),
        ('-1,2,\\sqrt 2', 60, '4,28,10', 90, '12,1,12'),
        ('3,7,-2', 120, '6,1,18', 120, '4,13,16'),
        ('2,-3,\\sqrt 2', 270, '2,4,4', 120, '5,20,4')
    ]

    def render(self):
        return 'Точку $p=({})$ поворачивают сначала на ${}$ градусов вокруг вектора $({})^\\top$, ' \
               'а потом на ${}$ градусов вокруг вектора $({})^\\top$, ' \
               'где поворот вокруг вектора значит поворот вокруг задаваемой им оси, и, ' \
               'если стрелочка смотрит на нас, то против часовой стрелки. ' \
               'Опишите эти вращения как единичные кватернионы и вычислите координаты точки, ' \
               'в которую перешла $p$.'.format(
            *self.text
        )
        # return 'A point $p=({})$ is first rotated by ${}$ degrees around the vector $({})^\\top$, ' \
        #        'and then by ${}$ degrees around the vector $({})^\\top$, ' \
        #        'where the rotation around the vector is understood as the rotation around the axis spanned by it and ' \
        #        'is counter-clockwise if the vector points toward the oberver. ' \
        #        'Describe these rotations via unit quaternions and compute the coordinates of the image of $p$.'.format(
        #     *self.text
        # )


class QuaternionRotations(Problem):
    def __init__(self):
        self.p, self.angle1, self.angle2, self.axis1, self.axis2 = self.gen_quaternion_rotations()

    def render(self):
        return 'Точку $p={}^\\top$ поворачивают сначала на ${}$ градусов вокруг вектора ${}^\\top$, ' \
               'а потом на ${}$ градусов вокруг вектора ${}^\\top$. ' \
               'Опишите эти вращения как единичные кватернионы и вычислите координаты точки, ' \
               'в которую перешла $p$.'.format(
            self.p,
            self.angle1,
            self.axis1,
            self.angle2,
            self.axis2
        )

    @staticmethod
    def gen_quaternion_rotations():
        angles = [90, 120]
        axis1 = [1,0,0]
        shuffle(axis1)
        axis2 = choice([[1,1,-1], [1,-1,-1]])
        shuffle(axis2)
        shuffle(angles)
        if angles[0] == 120:
            axis1, axis2 = axis2, axis1
        p = choice([[1,1,0], [2,1,1]])
        p = [choice((1, -1)) * c for c in p]
        shuffle(p)
        return tuple(p), angles[0], angles[1], tuple(axis1), tuple(axis2)
