from pool_problem import FromPoolProblem


class PermutationsSubgroups(FromPoolProblem):
    pool = []
    subpools = True

    def __init__(self):
        if not self.pool:
            problem_text = 'Рассмотрим в $S_4$ следующие перестановки:\n\\[ \\sigma={},\\quad \\tau={}. \\]\n' \
                           'Постройте явный изоморфизм между $\\langle \\sigma,\\tau \\rangle$ и какой-нибудь диэдральной группой,' \
                           ' если такой существует --- в противном случае докажите это.'
            permutations = [('(12)', '(13)(24)'),
                            ('(13)', '(12)(34)'),
                            ('(14)', '(12)(34)'),
                            ('(23)', '(12)(34)'),
                            ('(23)', '(13)(24)'),
                            # ('(12)', '(124)'),
                            # ('(13)', '(134)'),
                            # ('(24)', '(124)'),
                            # ('(24)', '(142)'),
                            # ('(12)', '(142)'),
                            # ('(13)', '(143)')
                            ]
            problems = [problem_text.format(*perm) for perm in permutations]
            self.pool.append(problems)
            problem_text = 'Используя общие теоретические соображения (в том числе возведение перестановок в степень) ' \
                           'и не более $5$ прямых умножений перестановок, докажите, что\n\\[ {}. \\]'
            problems = list(map(problem_text.format,
                                ['\\langle (123)(45), (145)(23) \\rangle = S_5',
                                 '\\langle (124), (2345) \\rangle = S_5',
                                 '\\langle (12345), (12)(34) \\rangle = A_5',
                                 '\\langle(1234), (2345)\\rangle = S_5',
                                 '\\langle(123)(45), (24)(35)\\rangle = S_5',
                                 '\\langle(123)(45), (13)(24)\\rangle = S_5']))
            self.pool.append(problems)
        super().__init__(quantity=1)
