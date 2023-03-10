class GaussInt:
    """Gaussian Integer functions.
    Functions implemented are:
         Arithmetic functions: +,*,/,%,**(exponentiation)
         a.gcd(b) - Compute the greatest common divisor of a and b.
         a.xgcd(b) - Extended gcd - return gcd(a,b) and x,y such that gcd(a,b)=xa+yb.
         n.isprime() - Is n prime (pseudoprime tests)
         n.factor() - Return a factor of n.
         n.factors() - Return list of the factors of n.
    Gaussian Integers can be created by:
         n = GaussInt(5,7)  # Create (5 + 7i)
         n = GaussInt(13)  # Create (5 + 0i)
         z = complex(2,3) n = GaussInt(z) # Round the complex number to integer form
    A list of the functions implemented in GaussInt is printed by the command help(GaussInt).
    Usage: from gaussint import * """

    def __init__(self, a=0, b=0):
        # if (type(a) == type(complex(1, 0))) and (b == 0):
        #     b = int(a.imag + 0.5);
        #     a = int(a.real + 0.5)
        self.r = int(a)
        self.i = int(b)

    def __str__(self):  # Overload string conversion used by print
        if self.i != 0:
            if self.i == 1:
                imag_str = 'i'
            elif self.i == -1:
                imag_str = '-i'
            else:
                imag_str = '{}i'.format(self.i)
        else:
            imag_str = ''
        return ''.join((str(self.r) if self.r != 0 else '', '+' if self.r != 0 and self.i > 0 else '', imag_str))

    def __repr__(self):  # Overload conversion used for output
        return "GaussInt(" + str(self.r) + ", " + str(self.i) + ")"

    def __complex__(self):  # Allow conversion to complex type
        return complex(self.r, self.i)

    def __eq__(self, other):  # Overload the "==" test operator
        return (self.r == other.r) and (self.i == other.i)

    def __ne__(self, other):  # Overload the "!=" test operator
        return not (self == other)

    def __bool__(self):
        return self != GaussInt(0, 0)

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(tuple(sorted(self.__dict__.items())))

    def norm(self):
        return self.r * self.r + self.i * self.i

    def __lt__(self, other):
        return self.norm() < other.norm()

    def add(self, summand):
        res = GaussInt()
        res.r = self.r + summand.r
        res.i = self.i + summand.i
        return res

    def __add__(self, summand):  # Overload the "+" operator
        if isinstance(summand, int):
            summand = GaussInt(summand)  # Coerce if adding integer and GaussInt
        return self.add(summand)

    def __radd__(self, summand):  # Overload the "+" operator
        if isinstance(summand, int):
            summand = GaussInt(summand)  # Coerce if adding integer and GaussInt
        return self.add(summand)

    def __iadd__(self, summand):  # Overload the "+=" operator
        self = self + summand
        return self

    def __neg__(self):  # Overload the "-" unary operator
        return GaussInt(-self.r, -self.i)

    def __sub__(self, summand):  # Overload the "-" binary operator
        return self.__add__(-summand)

    def __isub__(self, summand):  # Overload the "-=" operator
        self = self - summand
        return self

    def mult(self, multip):
        res = GaussInt()
        res.r = (self.r * multip.r) - (self.i * multip.i)
        res.i = (self.i * multip.r) + (self.r * multip.i)
        return res

    def __mul__(self, multip):  # Overload the "*" operator
        if isinstance(multip, int):
            multip = GaussInt(multip)  # Coerce if multiplying integer and GaussInt
        return self.mult(multip)

    def __rmul__(self, multip):  # Overload the "*" operator
        if isinstance(multip, int):
            multip = GaussInt(multip)  # Coerce if multiplying integer and GaussInt
        return self.mult(multip)

    def __imul__(self, multip):  # Overload the "*=" operator
        self = self * multip
        return self

    def div(self, divisor):
        if isinstance(divisor, int):
            divisor = GaussInt(divisor)  # Coerce if dividing GaussInt by integer
        q = complex(self.r, self.i) / complex(divisor.r, divisor.i)
        return GaussInt(int(round(q.real)), int(round(q.imag)))

    def __floordiv__(self, divisor):  # Overload the "/" operator
        return self.div(divisor)

    def __idiv__(self, divisor):  # Overload the "/=" operator
        self = self // divisor
        return self

    def mod(self, divisor):
        if isinstance(divisor, int):
            divisor = GaussInt(divisor)  # Coerce if dividing GaussInt by integer
        return self - divisor * (self // divisor)

    def __mod__(self, divisor):  # Overload the "%" operator
        return self.mod(divisor)

    def __imod__(self, divisor):  # Overload the "%=" operator
        self = self % divisor
        return self

    def divmod(self, divisor):
        if isinstance(divisor, int):
            divisor = GaussInt(divisor)  # Coerce if dividing GaussInt by integer
        q = self // divisor
        return q, self - divisor * q

    def powmod(self, exp, mod):
        accum = GaussInt(1, 0)
        basepow2 = self
        i = 0
        while (exp >> i) > 0:
            if ((exp >> i) & 1) == 1:
                accum = (accum * basepow2) % mod
            basepow2 = (basepow2 * basepow2) % mod
            i += 1
        return accum

    def pow(self, exp):
        accum = GaussInt(1, 0)
        basepow2 = self
        i = 0
        while (exp >> i) > 0:
            if ((exp >> i) & 1) == 1:
                accum = (accum * basepow2)
            basepow2 = (basepow2 * basepow2)
            i += 1
        return accum

    def __pow__(self, exponent):  # Overload the "**" operator
        return self.pow(exponent)
