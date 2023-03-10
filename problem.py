# from numpy.testing import assert_equal
from random import randint

class Problem:
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__
        # """Override the default Equals behavior"""
        # if isinstance(other, self.__class__):
        #     try:
        #         assert_equal(self.__dict__, other.__dict__)
        #     except AssertionError:
        #         return False
        #     else:
        #         return True
        # return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(tuple(sorted(self.__dict__.items())))


class TestProblem(Problem):
    def __init__(self):
        self.value = randint(1, 1000)

    def render(self):
        return 'Тестовая задача, value = {}'.format(self.value)