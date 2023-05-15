from problem import Problem
from random import choices
from common import monomial_to_tex


class SymmetricPolynomialRewrite(Problem):
    def __init__(self):
        self.n, self.monomials = self.gen_symmetric_polynomial()

    def render(self):
        return 'Представить симметрический многочлен ${}$ от $n={}$ переменных как многочлен от элементарных ' \
               'симметрических многочленов и как многочлен от полных однородных симметрических многочленов.'.format(
            '+'.join('{}+\\ldots'.format(monomial_to_tex(monom)) for monom in self.monomials),
            self.n
        )

    @staticmethod
    def gen_symmetric_polynomial():
        n = 4
        monomials = [0, 0]
        while monomials[0] == monomials[1]:
            monomials = [sorted(choices([4, 3, 2, 1], weights=[1, 2, 2, 2], k=3), reverse=True) for _ in range(2)]
        return n, monomials
