from problem import Problem
import sympy as sp
import random
from linear_algebra.common import good_charpoly, is_okay_charpoly
import itertools as it


class RecurrentSequenceJF(Problem):
    def __init__(self):
        self.coeffs, self.initial = self.gen_recurrent_sequence(3)

    def render(self):
        return 'Рекуррентная последовательность $a_n$ задана соотношениями\n' \
               '\[ a_{{n+1}} = {},\quad {}. \]\n' \
               'Найти явное выражение для $a_n$.'.format(
            ''.join('{}{}{}'.format('+' if c > 0 and i else '',
                                    c if abs(c) != 1 or i == len(self.coeffs) - 1 else ('-' if c == -1 else ''),
                                    'a_{{n{}}}'.format('-{}'.format(i) if i else '') if i != len(
                                        self.coeffs) - 1 else '') for
                    i, c in enumerate(self.coeffs)),
            ',\ '.join('a_{{{}}}=1'.format(i) for i in range(len(self.coeffs) - 1))
        )
        # return 'The recurrent sequence $a_n$ is given by\n' \
        #        '\[ a_{{n+1}} = {},\quad {}. \]\n' \
        #        'Find an explicit expression for $a_n$.'.format(
        #     ''.join('{}{}{}'.format('+' if c > 0 and i else '',
        #                             c if abs(c) != 1 or i == len(self.coeffs) - 1 else ('-' if c == -1 else ''),
        #                             'a_{{n{}}}'.format('-{}'.format(i) if i else '') if i != len(
        #                                 self.coeffs) - 1 else '') for
        #             i, c in enumerate(self.coeffs)),
        #     ',\ '.join('a_{{{}}}=1'.format(i) for i in range(len(self.coeffs) - 1))
        # )

    @staticmethod
    def gen_recurrent_sequence(length):
        n = length + 1
        flag = True
        ranvals = list(it.chain(*[[i, -i]*2 for i in range(1, 6)], [6, -6]))
        while flag:
            coeffs = random.choices(ranvals, k=n)
            m = sp.Matrix(length + 1, length + 1,
                          lambda i, j: coeffs[j] if i == 0 else 1 if i == j + 1 and i != length or i == j and i == length else 0)
            r = is_okay_charpoly(m)
            if r:
                b = m - r * sp.eye(n)
                bp = b
                d_prev = n
                d_new = b.rank()
                ds = []
                while d_prev != d_new:
                    ds.append(d_prev)
                    d_prev = d_new
                    bp *= b
                    d_new = bp.rank()
                ds.extend([d_new, d_new])
                blocks_sizes = tuple(ds[i] - 2 * ds[i - 1] + ds[i - 2] for i in range(2, len(ds)))
                flag = not blocks_sizes in [(0, 0, 0, 1), (1, 0, 1), (0, 0, 1), (0, 1, 1), (1, 0, 0, 1), (2, 0, 1), (1, 2), (0, 2)]
        return coeffs, 0
