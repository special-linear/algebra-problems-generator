from problem import Problem
from random import choice
import tomli


class FromListProblem(Problem):

    problems = None
    problems_source = None

    def __init__(self, number=None):
        if self.problems is None and self.problems_source is not None:
            with open(self.problems_source[0], "rb") as f:
                self.__class__.problems = tomli.load(f)[self.problems_source[1]]
        if self.problems is not None:
            if number is not None:
                if isinstance(number, int):
                    if number >= 0:
                        self.text = self.problems[number]
                    else:
                        if not hasattr(self, 'last_problem_number'):
                            self.__class__.last_problem_number = number
                        self.__class__.last_problem_number = (self.last_problem_number + 1) % len(self.problems)
                        self.text = self.problems[self.last_problem_number]
                else:
                    raise ValueError('Problem number is not an integer.')
            else:
                self.text = choice(self.problems)
        else:
            raise NotImplementedError('List of problems does not exist.')

    def render(self):
        return self.text
