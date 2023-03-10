from pool_problem import FromPoolProblem


class NormalOperatorsTheory(FromPoolProblem):
    pool = [
        [
            'Каков канонический вид и геометрический смысл ортогонального самосопряженного оператора?',
            'Пусть $A$ --- антисимметрическая матрица. Докажите, что $-A^2$ симметрическая.',
            'Пусть обратимая матрица $A$ антисимметрическая. Докажите, что $A^{-1}$ тоже антисимметрическая.',
            'Пусть оператор $\\varphi$ самосопряженный. Докажите, что $v+i\\varphi(v)=0$ только для $v=0$.'
        ],
        [
            'Классифицируйте и опишите геометрический смысл ортогональных антисимметрических матриц.',
            'Что представляют собой унитарные симметрические матрицы?',
            'Докажите, что ненулевые собственные числа антисимметрической матрицы являются чисто мнимыми.'
        ],
        [
            'Докажите, что равенство $\\langle x,Ax\\rangle = 0$ выполняется для всех $x$ только если $A$ антисимметрическая.',
            'Пусть $\\varphi$ и $\\psi$ --- нормальные операторы. Докажите, что если $\\varphi\\psi=0$, то $\\psi\\varphi=0$.',
            'Докажите, что если нормальный оператор $\\varphi$ коммутирует с нормальным оператором $\\psi$, то он коммутирует и с $\\psi^*$.'
        ]
    ]

    subpools = True
