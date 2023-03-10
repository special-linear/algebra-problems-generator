from problem import Problem
from random import randint, choice, sample
from numbertheory.common import extgcd


class ComplexPlotEasy(Problem):
    def __init__(self, parameters):
        self.num1, self.denom1, self.num2, self.denom2, self.arg_z, \
            self.lower_num, self.lower_denom, self.upper_num, self.upper_denom, \
            self.abs_z, self.transform_z = self.gen_complexplot(*parameters)

    @staticmethod
    def gen_complexplot(arg_denom_limit, abs_lower_limit, abs_upper_limit):
        # генерируем ограничения на аргумент
        denom1, denom2 = sample(range(2, arg_denom_limit), 2)
        num1, num2 = 0, 0
        while num1*denom2 >= num2*denom1 or num1 == denom1 or num2 == denom2:
            num1 = randint(1, 2*denom1-1)
            num2 = randint(1, 2*denom2-1)
        gcd1 = extgcd(num1, denom1)[0]
        gcd2 = extgcd(num2, denom2)[0]
        # на аргумент чего
        arg_z = choice(['iz+1', 'iz-1', 'iz+2', 'iz-2', '1-z', '2-z', '1-iz'])
        # генерируем ограничения на модуль
        abs_lower_num, abs_upper_num = 0, 0
        while abs_lower_num == abs_upper_num:
            abs_lower_num, abs_upper_num = sorted([randint(abs_lower_limit, abs_upper_limit) for _ in (0, 0)])
        abs_denum = randint(1, 6)
        gcd_lower = extgcd(abs_lower_num, abs_denum)[0]
        gcd_upper = extgcd(abs_upper_num, abs_denum)[0]
        # на модуль чего
        abs_z = choice(['z+1', 'z-1', 'z+i', 'z-i'])
        # как преобразуем
        transform_z = (choice(['\\frac{2\pi i}{3}', '\\frac{-2\pi i}{3}', '\\frac{\pi i}{3}', '\\frac{-\pi i}{3}',
                               '\\frac{\pi i}{4}', '\\frac{-\pi i}{4}', '\\frac{3\pi i}{4}', '\\frac{-3\pi i}{4}']),
                       choice(['z+i', 'z-i', 'z+1', 'z-1']),
                       choice(['+i', '-i']))
        return num1//gcd1, denom1//gcd1, num2//gcd2, denom2//gcd2, \
               arg_z, \
               abs_lower_num//gcd_lower, abs_denum//gcd_lower, abs_upper_num//gcd_upper, abs_denum//gcd_upper, \
               abs_z, \
               transform_z

    @staticmethod
    def display_fraction(num, denom):
        if denom != 1:
            return '\\frac{{{}}}{{{}}}'.format(num, denom)
        else:
            return '{}'.format(num)


    def render(self):
        assumptions = '{}\pi \leqslant \\arg({}) \leqslant {}\pi\quad \\text{{и}}\quad {} \leqslant |{}| \leqslant {}'.format(
            self.display_fraction(self.num1, self.denom1),
            self.arg_z,
            self.display_fraction(self.num2, self.denom2),
            self.display_fraction(self.lower_num, self.lower_denom),
            self.abs_z,
            self.display_fraction(self.upper_num, self.upper_denom)
        )
        transformation = '\overline{{\exp\left( {} \\right)\cdot({})}} {}'.format(
            *self.transform_z
        )
        return 'Изобразить на комплексной плоскости множество точек\n' \
               '\[ \left\{{ {} \ \middle|\ {} \\right\}} \]'.format(transformation, assumptions)
        # return 'Plot the following subset of the complex plane:\n' \
        #        '\[ \left\{{ {} \ \middle|\ {} \\right\}} \]'.format(transformation, assumptions)


class ComplexPlotHard(Problem):
    def __init__(self, number=None):
        self.assumption = choice(self.assumptions)
        self.transformation = choice(self.transformations)

    assumptions = [
        '(z+\overline{z})^2=z\overline{z}',
        'z^2+\overline{z}^2=2|z|^2',
        'z+z^{-1}\in\mathbb{R}',
        '(1+i)\overline{z}+(1-i)z=|1+i|',
        '(1+i)\overline{z}+(1-i)z=|1+i|\cdot i',
        '|z|\leqslant\operatorname{Re}(z)+\operatorname{Im}(z)',
        '\\arg\left(\\frac{z-i}{z+i}\\right)=\\frac{\pi}{4}',
        '\\frac{|z|}{z}+1=z-\overline{z}',
        '|z-1|^2+|z+1|^2=4',
        '|z-1-i|=2\cdot|z+1-i|',
        '\\arg{z}=\\frac{\pi}{2}\ \\text{и}\ \left|z+\\frac{2}{z}\\right|\leqslant1',
        '\\arg{z}=\\frac{3\pi}{2}\ \\text{и}\ \left|z-\\frac{3}{z}\\right|\leqslant4'
    ]
    transformations = [
        '\overline{iz+1}^2-i',
        '(z-1)\cdot(1+i)',
        '\\frac{z+1}{\overline{z+1}',
        'z+\operatorname{Im}({z})\cdot i-1',
        '\\frac{z}{i-2}+1-i',
        '(z^2-i)\cdot(i-1)+2',
        'z^2-\overline{z}',
        '1-i\cdot\overline{z}'
    ]

    def render(self):
        return 'Изобразить на комплексной плоскости множество точек\\\\' \
               '\[ \left\{{ {} \,\middle|\, {} \\right\}} \]'.format(self.transformations, self.assumption)