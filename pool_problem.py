from problem import Problem
import itertools as it
from random import sample, randint


class FromPoolProblem(Problem):

    pool = [[None]]

    subpools = False

    short_options = False

    multiplicity = 1

    def __init__(self, quantity=0):
        if self.subpools:
            self.problems = list(it.chain.from_iterable(sample(subpool, k=min(quantity or len(subpool) // 2, len(subpool))) for subpool in self.pool))
        else:
            self.problems = sample(self.pool, k=min(quantity or len(self.pool) // 2, len(self.pool)))
        self.inner_degree_of_freedom = randint(1, self.multiplicity)

    def render(self):
        enumerate_env_name = 'enumerate{}'.format('*' if self.short_options else '')
        enumerate_env_options = '[itemjoin=\\qquad]' if self.short_options else ''
        enumerate_align = ('\\begin{center}', '\\end{center}') if self.short_options else ('\\leavevmode', '')
        return '{0} \\begin{{{2}}}{3} {4} \\end{{{2}}}{1}'.format(
            *enumerate_align, enumerate_env_name, enumerate_env_options,
            ' '.join('\\item {}'.format(s) for s in self.problems))
