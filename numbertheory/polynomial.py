from fractions import Fraction


class Polynomial:

    @staticmethod
    def strip_polynomial_list(poly):
        while poly and not poly[0]:
            poly.pop(0)
        return poly or [Fraction(0)]

    def __init__(self, coefficients=(), variable='t'):
        self.coefficients = tuple(self.strip_polynomial_list(list(coefficients)))
        self.variable = variable

    def deg(self):
        return len(self.coefficients)-1

    def __str__(self):  # Overload string conversion used by print
        # print(self.coefficients)
        monomials_strings = []
        for i, c in enumerate(self.coefficients):
            monom_str = ''
            if i != self.deg():
                if c > 0 and i != 0:
                    monom_str += '+'
                if c != 0:
                    coeff_str = str(c) if c not in (1, -1) else str(c)[:-1]
                    # print('c =',str(c))
                    # coeff_str = str(c)
                    power = self.deg()-i
                    power_str = '^{{{}}}'.format(power) if power != 1 else ''
                    monom_str += '{}{}{}'.format(coeff_str, self.variable, power_str)
            else:
                if c > 0 and self.deg() != 0:
                    monom_str += '+'
                if c != 0:
                    monom_str += '{}'.format(str(c))
                if c == 0 and i == 0:
                    monom_str += '0'
            monomials_strings.append(monom_str)
        return "".join(monomials_strings)

    def __repr__(self):  # Overload conversion used for output
        return 'Polynomial({})'.format(self.coefficients)

    def __eq__(self, other):  # Overload the "==" test operator
        return self.coefficients == other.coefficients and self.variable == other.variable

    def __ne__(self, other):  # Overload the "!=" test operator
        return not (self == other)

    def __lt__(self, other):
        return self.deg() < other.deg()

    def __bool__(self):
        return self.coefficients and self.coefficients != (0,)

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(tuple(sorted(self.__dict__.items())))

    def add(self, summand):
        if isinstance(summand, int) or isinstance(summand, Fraction):
            summand = Polynomial([summand])
        if self.deg() >= summand.deg():
            f, g = self, summand
        else:
            f, g = summand, self
        sum_coefficients = [0 for _ in range(f.deg()+1)]
        for i in range(-1, -f.deg()-2, -1):
            if i >= -g.deg()-1:
                sum_coefficients[i] = f.coefficients[i] + g.coefficients[i]
            else:
                sum_coefficients[i] = f.coefficients[i]
        return Polynomial(sum_coefficients)

    def __add__(self, summand):  # Overload the "+" operator
        return self.add(summand)

    def __radd__(self, summand):  # Overload the "+" operator
        return self.add(summand)

    def __iadd__(self, summand):  # Overload the "+=" operator
        self = self + summand
        return self

    def __neg__(self):  # Overload the "-" unary operator
        return Polynomial(list(map(lambda x: -x, self.coefficients)))

    def __sub__(self, summand):  # Overload the "-" binary operator
        return self.__add__(-summand)

    def __isub__(self, summand):  # Overload the "-=" operator
        self = self - summand
        return self

    def mult(self, multip):
        if isinstance(multip, int) or isinstance(multip, Fraction):
            multip = Polynomial([multip])
        a = self.coefficients
        b = multip.coefficients
        ab = []
        for deg in range(len(a) + len(b) - 1):
            ab.append(sum(a[i] * b[deg - i] for i in range(deg + 1) if 0 <= i < len(a) and 0 <= deg - i < len(b)))
        return Polynomial(ab)

    def __mul__(self, multip):  # Overload the "*" operator
        return self.mult(multip)

    def __rmul__(self, multip):  # Overload the "*" operator
        return self.mult(multip)

    def __imul__(self, multip):  # Overload the "*=" operator
        self = self * multip
        return self

    def divmod(self, divisor):
        out = list(map(Fraction, self.coefficients))  # Copy the dividend
        divisor = list(map(Fraction, divisor.coefficients))
        normalizer = divisor[0]
        for i in range(len(self.coefficients) - (len(divisor) - 1)):
            out[i] /= normalizer  # for general polynomial division (when polynomials are non-monic),
            # we need to normalize by dividing the coefficient with the divisor's first coefficient
            coef = out[i]
            if coef != 0:  # useless to multiply if coef is 0
                for j in range(1, len(
                        divisor)):  # in synthetic division, we always skip the first coefficient of the divisor,
                    # because it's only used to normalize the dividend coefficients
                    out[i + j] += -divisor[j] * coef
        # The resulting out contains both the quotient and the remainder, the remainder being the size of the divisor
        # (the remainder has the same degree as the divisor since it's what we couldn't divide from the dividend),
        # so we compute the index where this separation is, and return the quotient and remainder.
        separator = -(len(divisor) - 1)
        return Polynomial(out[:separator]), Polynomial(out[separator:])  # return quotient, remainder.

    def __floordiv__(self, divisor):  # Overload the "/" operator
        return self.divmod(divisor)[0]

    def __idiv__(self, divisor):  # Overload the "/=" operator
        self = self // divisor
        return self

    def __mod__(self, divisor):  # Overload the "%" operator
        return self.divmod(divisor)[1]

    def __imod__(self, divisor):  # Overload the "%=" operator
        self = self % divisor
        return self

    def __call__(self, a):
        val = 0
        for c in self.coefficients:
            val *= a
            val += c
        return val
