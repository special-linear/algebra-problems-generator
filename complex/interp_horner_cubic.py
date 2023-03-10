import os
from random import choice
from numbertheory.gaussint import GaussInt

from problem import Problem

with open(os.path.dirname(__file__)+'/interp-horner-cubic-data.txt', encoding='utf-8', mode='r') as problem_data_file:
    problem_data_str = problem_data_file.readlines()


class InterpolationHornerCubic(Problem):
    def __init__(self):
        data_line = choice(problem_data_str)
        xs_str, vs_str = data_line.split(' -> ')
        self.xs = map(lambda z: GaussInt(complex(z).real, complex(z).imag), xs_str.split(','))
        self.vs = map(lambda z: GaussInt(complex(z).real, complex(z).imag), vs_str.split(','))

    def render(self):
        xs_str = ' & '.join(map(str, self.xs))
        vs_str = ' & '.join(map(str, self.vs))
        return 'Про многочлен $f$ четвертой степени с целыми коэффициентами известно, ' \
               'что он принимает значения, указанные в таблице:\n' \
               '\\[ \\begin{{array}}{{c|ccccc}} x & {} \\\\\\hline f(x) & {}  \\end{{array}} \\]\n' \
               'Кроме того, известно, что у $f$ имеется рациональный корень.\n' \
               'Найдите все четыре корня многочлена $f$.'.format(xs_str, vs_str)
