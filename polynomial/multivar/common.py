def monomial_to_tex(monom, variables=None):
    if variables is None:
        variables = ['x_{{{}}}'.format(i + 1) for i in range(len(monom))]
    return ''.join('{}^{{{}}}'.format(v, d) for v, d in zip(variables, monom))
