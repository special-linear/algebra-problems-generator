from random import randint, shuffle, sample

from numbertheory.common import extgcd
from problem import Problem

import sympy as sp


class CRTSystem(Problem):
    def __init__(self, parameters=(4, 25, 90)):
        self.coefficients = self.gen_crt_system(*parameters)

    def render(self):
        system_str = ',\\\\\n'.join(['x \equiv {} & \pmod{{{}}}'.format(*cong) for cong in self.coefficients])
        return 'Решить систему линейных сравнений:\n' \
               '\\[ \\begin{{cases}}\n{}. \n\\end{{cases}} \\]'.format(system_str)
        # return 'Solve the system of linear congruences:\n' \
        #        '\\[ \\begin{{cases}}\n{}.\n\\end{{cases}} \\]'.format(system_str)

    @staticmethod
    def gen_crt_system(cong_number, limit_lower, limit_upper):
        m_list = set()
        while len(m_list) < cong_number:
            m_list.add(randint(limit_lower, limit_upper))
        m_list = list(m_list)
        gcd_set = []
        for i in range(cong_number):
            gcd_set.append([])
            for j in range(cong_number):
                gcd_set[i].append(extgcd(m_list[i], m_list[j])[0])
        r_list = []
        rems_are_good = False
        while not rems_are_good:
            r_list = [randint(2, m - 1) for m in m_list]
            rems_are_good = True
            for i in range(cong_number):
                for j in range(i):
                    mij = gcd_set[i][j]
                    rems_are_good = rems_are_good and (r_list[i] % mij == r_list[j] % mij)
        return tuple(zip(tuple(r_list), tuple(m_list)))


class CRTTheory(Problem):
    def __init__(self):
        self.coefficients = self.gen_crt_system()

    def render(self):
        system_str = ', \\\\ '.join(['{}x \equiv {} & \pmod{{{}}}'.format(c if c != 1 else '', r, m) for c, r, m in self.coefficients])
        return 'Дана система линейных сравнений: ' \
               '\\[ \\begin{{cases}} {}. \\end{{cases}} \\] ' \
               'Приведите систему к виду, в котором можно пытаться напрямую применить китайскую теорему о  остатках ' \
               '(не меняя числа сравнений). Найдите в ней подсистему из {} сравнений, имеющую решение.'.format(
            system_str, 3
        )

    @staticmethod
    def gen_crt_system():
        ps = list(sp.primerange(2, 18))
        shuffle(ps)
        mods = (ps[0] * ps[1], ps[0] * ps[2], ps[1] * ps[3] * ps[4], ps[4] * ps[5], ps[5] * ps[6])
        rs = [randint(1, m - 1) for m in mods]
        cs = [1] * len(mods)
        for i in sample(range(len(mods)), k=2):
            c = mods[i]
            while sp.gcd(c, mods[i]) != 1:
                c = randint(2, mods[i] - 1)
            cs[i] = c
            rs[i] = (rs[i] * c) % mods[i]
        return tuple(zip(cs, rs, mods))