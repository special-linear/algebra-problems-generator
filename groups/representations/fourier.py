from problem import Problem
from list_problem import FromListProblem
from random import choice, choices


class BooleanCubeFourier(Problem):
    def __init__(self):
        self.p1, self.p2 = self.gen_boolean_cube_fourier()

    def render(self):
        return 'На трехмерном булевом кубе $\\{{0,1\\}}^3$ задана функция\n' \
               '\\[ f(x) = \\mathrm{{dist}}\\big(x,{}\\big) - ' \
               '\\mathrm{{dist}}\\big(x,{}\\big), \\]\n' \
               'где $\\mathrm{{dist}}$ --- расстояние по Хэммингу. ' \
               'Вычислить ее преобразование Фурье $\\widehat{{f}}$ и использовать его для вычисления ' \
               '$f^{{*10}}$ (свертка с собой $9$ раз). При желании вычисления с рациональным числами можно заменить ' \
               'вычислениями с десятичными дробями с точностью до пятого знака после запятой.'.format(
            self.p1, self.p2
        )

    @staticmethod
    def gen_boolean_cube_fourier():
        p1, p2 = (0, 0, 0), (0, 0, 0)
        while sum(abs(a-b) for a, b in zip(p1, p2)) < 2:
            p1, p2 = (choices((0, 1), k=3) for _ in range(2))
        return tuple(p1), tuple(p2)


class FourierS3(FromListProblem):
    problems = [
        # '\\operatorname{ord}(\\sigma)\\cdot\\min\\{i=1,\\ldots,4 \\mid \\sigma(i)=i \\}',
        # '\\operatorname{ord}(\\sigma)\\cdot\\min\\{i=1,\\ldots,4 \\mid \\sigma(i)\\neq i \\}',
        # '\\operatorname{ord}(\\sigma)+\\min\\{i=1,\\ldots,4 \\mid \\sigma(i)=i \\}',
        # '\\operatorname{ord}(\\sigma)+\\min\\{i=1,\\ldots,4 \\mid \\sigma(i)\\neq i \\}',
        # '|\\sigma^{S_3}|\\cdot\\min\\{i=1,\\ldots,4 \\mid \\sigma(i)=i \\}',
        # '|\\sigma^{S_3}|\\cdot\\min\\{i=1,\\ldots,4 \\mid \\sigma(i)\\neq i \\}',
        # '|\\sigma^{S_3}|+\\min\\{i=1,\\ldots,4 \\mid \\sigma(i)=i \\}',
        # '|\\sigma^{S_3}|+\\min\\{i=1,\\ldots,4 \\mid \\sigma(i)\\neq i \\}',
        # '\\operatorname{sgn}(\\sigma)+\\min\\{i=1,\\ldots,4 \\mid \\sigma(i)=i \\}',
        # '\\operatorname{sgn}(\\sigma)+\\min\\{i=1,\\ldots,4 \\mid \\sigma(i)\\neq i \\}',
        '\\operatorname{sgn}(\\sigma) \\cdot |\\sigma^{S_3}| + \\operatorname{inv}(\\sigma)',
        '\\operatorname{sgn}(\\sigma) + |\\sigma^{S_3}| \\cdot \\operatorname{inv}(\\sigma)',
        '\\operatorname{sgn}(\\sigma)\\cdot |\\sigma^{S_3}| - \\operatorname{inv}(\\sigma)',
    ]

    def render(self):
        return 'На группе $S_3$ задана функция $f$\n\\[ f(\\sigma) = {}. \\]\n' \
               'Для каждого неприводимого представления $S_3$ выбрать какой-нибудь ортогональный базис ' \
               'на пространстве представления, выразить в этом базисе матрицы, отвечающие всем элементам группы, ' \
               'и вычислить преобразования Фурье функций $f$ и $f*f$. Напомним, преобразование Фурье можно записать ' \
               'как одну матрицу размера $d\\times d$ для каждого представления размерности $d$.'.format(
            self.text
        )