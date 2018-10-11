import random

from CryptographyLib import util
from CryptographyLib import exception


class Polynomial:
    """
    this class is an number type, which is Polynomial
    each Polynomial instant is an Polynomial type number
    the calculate of Polynomial's coefficients is on the Z_2^+
    the add, sub, mul, div, mod can be calculate with or without an polynomial
    the multiplicative inverse calculate with an polynomial
    """
    # all the operators on the calculation internal use int but not class Polynomial
    # however, the interface use class Polynomial class
    expression = None

    def __init__(self, e):
        """
        :param e: the coefficient express using bit
        """
        self.expression = e

    def __str__(self):
        return str(self.expression)

    def add(self, x, modFunc=None):
        if not isinstance(x, Polynomial):
            raise TypeError
        if not isinstance(modFunc, Polynomial) and modFunc is not None:
            raise TypeError
        v = Polynomial.__add__(x.expression, self.expression)
        if modFunc:
            return Polynomial(self.__modAndDiv__(v, modFunc.expression)[0])
        else:
            return Polynomial(v)

    def sub(self, x, modFunc=None):
        return self.add(x, modFunc)

    def mul(self, x, modFunc=None):
        if not isinstance(x, Polynomial):
            raise TypeError
        if not isinstance(modFunc, Polynomial) and modFunc is not None:
            raise TypeError
        x.__validityTest__()
        self.__validityTest__()
        v = self.__mul__(x.expression, self.expression)
        if modFunc:
            return Polynomial(self.__modAndDiv__(v, modFunc.expression)[0])
        else:
            return Polynomial(v)

    def div(self, x):
        if not isinstance(x, Polynomial):
            raise TypeError
        x.__validityTest__()
        self.__validityTest__()
        return Polynomial(Polynomial.__modAndDiv__(self.expression, x.expression)[1])

    def mod(self, x):
        if not isinstance(x, Polynomial):
            raise TypeError
        x.__validityTest__()
        self.__validityTest__()
        return Polynomial(Polynomial.__modAndDiv__(self.expression, x.expression)[0])

    def __validityTest__(self):
        if self.expression < 0:
            raise exception.NegativePolynomialExpression

    @staticmethod
    def __add__(x, y):
        return x ^ y

    @staticmethod
    def __sub__(x, y):
        return x ^ y

    @staticmethod
    def __mul__(x, y):
        ans = 0
        while y:
            if y & 1:
                ans = Polynomial.__add__(ans, x)
            x *= 2
            y //= 2
        return ans

    @staticmethod
    def __modAndDiv__(x, y):
        """
        return the (x%y, x/y)
        """
        if y == 0:
            raise ZeroDivisionError
        xl = util.bitLen(x)
        yl = util.bitLen(y)
        if xl < yl:
            return x, 0
        d = 0
        while xl >= yl:
            x, d = Polynomial.__sub__(x, y << (xl - yl)), Polynomial.__add__(d, (1 << (xl - yl)))
            xl = util.bitLen(x)
        return x, d

    def gcd(self, x):
        if not isinstance(x, Polynomial):
            raise TypeError
        x.__validityTest__()
        self.__validityTest__()
        v = x.expression
        w = self.expression
        while w:
            t = Polynomial.__modAndDiv__(v, w)[0]
            v = w
            w = t
        return Polynomial(v)

    def extendGcd(self, x):
        """
        calculate ax+bSelf = gcd(x, self)
        return (a, b, gcd)
        """
        if not isinstance(x, Polynomial):
            raise TypeError
        self.__validityTest__()
        x.__validityTest__()
        v, w = x.expression, self.expression
        x1, x2, y1, y2 = 1, 0, 0, 1
        while w:
            t = self.__modAndDiv__(v, w)
            v, w = w, t[0]
            t1, t2 = y1, y2
            y1 = Polynomial.__sub__(x1, Polynomial.__mul__(y1, t[1]))
            y2 = Polynomial.__sub__(x2, Polynomial.__mul__(y2, t[1]))
            x1, x2 = t1, t2
            # print(x1, x2, y1, y2, v, w)
            # assert Polynomial.__add__(Polynomial.__mul__(x1, x.expression),
            #                           Polynomial.__mul__(x2, self.expression)) == v
        return Polynomial(x1), Polynomial(x2), Polynomial(v)

    def mulInverse(self, x):
        if not isinstance(x, Polynomial):
            raise TypeError
        self.__validityTest__()
        x.__validityTest__()
        if x.expression == 1:
            raise exception.MultiplicativeInverseUseModulusOne
        r1, r2, r3 = self.extendGcd(x)
        if r3.expression != 1:
            return Polynomial(-1)
        return r2

    def equal(self, x):
        return self.expression == x.expression


if __name__ == "__main__":
    p = Polynomial(0x2)
    print(hex((p.mulInverse(Polynomial(0x11b))).expression))
    exit(0)
    while True:
        p1 = Polynomial(random.randint(1, 0xffff))
        p2 = Polynomial(random.randint(1, 0xffff))
        p3 = p1.add(p2)
        p4 = p3.sub(p2)
        p5 = p3.sub(p1)
        print(p1.expression, p2.expression, p3.expression, p4.expression, p5.expression)
        assert p1.equal(p4)
        assert p2.equal(p5)
        p3 = p1.mul(p2)
        p4 = p3.div(p1)
        p5 = p3.div(p2)
        print(p1.expression, p2.expression, p3.expression, p4.expression, p5.expression)
        assert p4.equal(p2)
        assert p5.equal(p1)
        p6 = p1.div(p2)
        p7 = p1.mod(p2)
        assert p6.mul(p2).add(p7).equal(p1)
        p8, p9, p10 = p1.extendGcd(p2)
        print(p1.expression, p2.expression, p8.expression, p9.expression, p10.expression, p1.gcd(p2).expression)
        p11 = p8.mul(p2).add(p9.mul(p1))
        print(p11.expression)
        assert p11.equal(p10)
        if p2.expression == 1:
            continue
        p12 = p1.mulInverse(p2)
        print(p12, p1, p2)
        if p12.expression != -1:
            assert p12.mul(p1, p2).equal(Polynomial(1))
