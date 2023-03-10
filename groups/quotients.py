from pool_problem import FromPoolProblem


class QuotientGroup(FromPoolProblem):
    pool = [
        [
            'Пусть $G=(\\mathbb{R},+)$, $H=(\\mathbb{Z},+)$, $F=\\{z\\in\\mathbb{C}\mid |z|=1\\}$. Докажите, что $G/H\\cong F$.',
            'Пусть $G=(\\mathbb{R}\\setminus\\{0\\},*)$, $H\\leqslant G$ --- подгруппа порядка $2$, $F=(\\mathbb{R},+)$. Докажите, что $G/H\\cong F$.',
            'Пусть $G$ --- группа квадратных вещественных обратимых верхне-треугольных матриц, а $H\\leqslant G$ --- подгруппа матриц с единицами на главной диагонали. Докажите, что $H$ нормальна в $G$ и что $G/H$ коммутативна.',
            'Пусть все элементы групп $H$ и $G/H$ имеют конечные порядки. Докажите, что то же имеет место для всех элементов группы $G$.',
        ],
        list(map(lambda groups: 'Вычислить фактор-группу $G/H$, где\n\\[ G={},\\quad H={}. \\]'.format(*groups),
                 [('\\operatorname{M}(2,\\mathbb{R})^+', '\\left\\{\\begin{pmatrix}\\alpha&\\beta\\\\\\gamma&-\\alpha\\end{pmatrix}\\,\\middle|\\, \\alpha,\\beta,\\gamma\\in\\mathbb{R}\\right\\}'),
                  ('\\operatorname{M}(2,\\mathbb{R})^+', '\\left\\{\\begin{pmatrix}\\alpha&\\beta\\\\\\gamma&\\delta\\end{pmatrix}\\,\\middle|\\, \\alpha+\\beta+\\gamma+\\delta=0\\right\\}'),
                  ('\\operatorname{M}(2,\\mathbb{C})^+', '\\operatorname{M}(2,\\mathbb{R})^+'),
                  ('\\mathbb{C}^*', '\\{z\\in\\mathbb{C}\\mid|z|=1\\}'),
                  ('\\mathbb{C}^*', '\\{z\\in\\mathbb{C}^*\\mid \\operatorname{Re}(z)\\operatorname{Im}(z)=0\\}'),
                  ('\\{ A\\in\\operatorname{M}(n,\\mathbb{R}\\mid A\\text{ диагональная}', '\\{ \\lambda I_n\\mid\\lambda\\in\\mathbb{R}\\}'),
                  ('\\{ A\\in\\operatorname{GL}(n,\\mathbb{R}\\mid A\\text{ диагональная}', '\\{ \\lambda I_n\\mid\\lambda\\in\\mathbb{R}^*\\}')])),
        list(map(lambda groups: 'Вычислить фактор-группу $G/H$, где\n\\[ G={},\\quad H={}. \\]'.format(*groups),
                         [('\\operatorname{GL}(n,\\mathbb{R})', '\\{A\\in\\operatorname{M}(n,\\mathbb{R})\\mid \\det(A)=\\pm 1\\}'),
                          ('\\operatorname{GL}(n,\\mathbb{R})', '\\{A\\in\\operatorname{M}(n,\\mathbb{R})\\mid \\det(A)>0\\}'),
                          ('\\operatorname{GL}(n,\\mathbb{C})', '\\{A\\in\\operatorname{M}(n,\\mathbb{C})\\mid \\det(A)\\in\\mathbb{R}\\}'),
                          ('\\operatorname{GL}(n,\\mathbb{C})', '\\{A\\in\\operatorname{M}(n,\\mathbb{C})\\mid \\det(A)\\in\\mathbb{R}_{>0}\\}'),
                          ('\\operatorname{GL}(n,\\mathbb{C})', '\\{A\\in\\operatorname{M}(n,\\mathbb{C})\\mid |\\det(A)|=1\\}')])),
    ]
    subpools = True