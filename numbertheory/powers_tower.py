from random import randint
from math import gcd

from problem import Problem


class PowersTower(Problem):

    def __init__(self, parameters=(3, 100, 300, 200, 300)):
        self.powers, self.m = self.gen_powers_tower(*parameters)

    @staticmethod
    def tower_to_tex(powers):
        if len(powers) == 1:
            return str(powers[0])
        else:
            return '{}^{{{}}}'.format(powers[0], PowersTower.tower_to_tex(powers[1:]))

    def render(self):
        return 'Вычислить остаток\n' \
               '\\[ {} \\pmod{{{}}}. \\]'.format(self.tower_to_tex(self.powers), self.m)
        # return 'Calculate the remainder\n' \
        #        '\\[ {} \\pmod{{{}}}. \\]'.format(self.tower_to_tex(self.powers), self.m)

    @staticmethod
    def gen_powers_tower(height, limit_lower, limit_upper, mod_lower, mod_upper):
        while True:
            t = [randint(limit_lower, limit_upper) for _ in range(height)]
            m = randint(mod_lower, mod_upper)
            if gcd(t[0], m) == 1:
                c = randint(3, 9)
                t[0] *= c
                m *= c
                return tuple(t), m

