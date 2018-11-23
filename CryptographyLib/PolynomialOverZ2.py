import logging
import random

from CryptographyLib import util
from CryptographyLib import exception


class PolynomialOverZ2:
    """
    this class is an number type, which is Polynomial
    each Polynomial instant is an Polynomial type number
    the calculate of Polynomial's coefficients is on the Z_2^+
    the add, sub, mul, div, mod can be calculate with or without an polynomial as modulus
    the multiplicative inverse calculate with an polynomial as modulus

    use the coefficient's hex expression to init the object and
    can get this expression use int(poly_obj) or innerExpression

    for that the '+', '*', '/', '%' has only two operand,
    so there are add(), mul(), div() etc.
    """

    # all the operators on the calculation internal use int but not class Polynomial
    # however, the interface use class Polynomial class

    def __init__(self, e):
        """
        :param e: the coefficient express using bit
        """
        self.__expression = e

    def __str__(self):
        return hex(self.__expression)

    def __repr__(self):
        return hex(self.__expression)

    def __lt__(self, other):
        return self.__expression < other.__expression

    def __eq__(self, other):
        return self.__expression == other.__expression

    def __hash__(self):
        return self.__expression

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.sub(other)

    def __mul__(self, other):
        return self.mul(other)

    def __floordiv__(self, other):
        return self.div(other)

    def __truediv__(self, other):
        return self.div(other)

    def __mod__(self, other):
        return self.mod(other)

    def __int__(self):
        return self.__expression

    def innerExpression(self):
        return self.__expression

    def add(self, x, modFunc=None):
        if not isinstance(x, PolynomialOverZ2):
            raise TypeError
        if not isinstance(modFunc, PolynomialOverZ2) and modFunc is not None:
            raise TypeError
        v = PolynomialOverZ2.__add(x.__expression, self.__expression)
        if modFunc:
            return PolynomialOverZ2(self.__modAndDiv(v, modFunc.__expression)[0])
        else:
            return PolynomialOverZ2(v)

    def sub(self, x, modFunc=None):
        return self.add(x, modFunc)

    def mul(self, x, modFunc=None):
        if not isinstance(x, PolynomialOverZ2):
            raise TypeError
        if not isinstance(modFunc, PolynomialOverZ2) and modFunc is not None:
            raise TypeError
        x.__validityTest()
        self.__validityTest()
        v = self.__mul(x.__expression, self.__expression)
        if modFunc:
            return PolynomialOverZ2(self.__modAndDiv(v, modFunc.__expression)[0])
        else:
            return PolynomialOverZ2(v)

    def fastMulWithMod(self, x, modFunc):
        if not isinstance(x, PolynomialOverZ2):
            raise TypeError
        if not isinstance(modFunc, PolynomialOverZ2) and modFunc is not None:
            raise TypeError
        x.__validityTest()
        self.__validityTest()
        v, w, ans = self.__expression, x.__expression, 0
        while w:
            if w & 1:
                ans = PolynomialOverZ2.__modAndDiv(ans ^ v, modFunc.__expression)[0]
            w, v = w // 2, PolynomialOverZ2.__modAndDiv(v * 2, modFunc.__expression)[0]
        return PolynomialOverZ2(ans)

    def div(self, x):
        if not isinstance(x, PolynomialOverZ2):
            raise TypeError
        x.__validityTest()
        self.__validityTest()
        return PolynomialOverZ2(PolynomialOverZ2.__modAndDiv(self.__expression, x.__expression)[1])

    def mod(self, x):
        if not isinstance(x, PolynomialOverZ2):
            raise TypeError
        x.__validityTest()
        self.__validityTest()
        return PolynomialOverZ2(PolynomialOverZ2.__modAndDiv(self.__expression, x.__expression)[0])

    def __validityTest(self):
        if self.__expression < 0:
            raise exception.NegativePolynomialExpression

    @staticmethod
    def __add(x, y):
        return x ^ y

    @staticmethod
    def __sub(x, y):
        return x ^ y

    @staticmethod
    def __mul(x, y):
        ans = 0
        while y:
            if y & 1:
                ans = PolynomialOverZ2.__add(ans, x)
            x *= 2
            y //= 2
        return ans

    @staticmethod
    def __modAndDiv(x, y):
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
            x, d = PolynomialOverZ2.__sub(x, y << (xl - yl)), PolynomialOverZ2.__add(d, (1 << (xl - yl)))
            xl = util.bitLen(x)
        return x, d

    def gcd(self, x):
        if not isinstance(x, PolynomialOverZ2):
            raise TypeError
        x.__validityTest()
        self.__validityTest()
        v = x.__expression
        w = self.__expression
        while w:
            t = PolynomialOverZ2.__modAndDiv(v, w)[0]
            v = w
            w = t
        return PolynomialOverZ2(v)

    def extendGcd(self, x):
        """
        calculate ax+bSelf = gcd(x, self)
        return (a, b, gcd)
        """
        if not isinstance(x, PolynomialOverZ2):
            raise TypeError
        self.__validityTest()
        x.__validityTest()
        v, w = x.__expression, self.__expression
        x1, x2, y1, y2 = 1, 0, 0, 1
        while w:
            t = self.__modAndDiv(v, w)
            v, w = w, t[0]
            t1, t2 = y1, y2
            y1 = PolynomialOverZ2.__sub(x1, PolynomialOverZ2.__mul(y1, t[1]))
            y2 = PolynomialOverZ2.__sub(x2, PolynomialOverZ2.__mul(y2, t[1]))
            x1, x2 = t1, t2
            # print(x1, x2, y1, y2, v, w)
            # assert Polynomial.__add__(Polynomial.__mul__(x1, x.expression),
            #                           Polynomial.__mul__(x2, self.expression)) == v
        return PolynomialOverZ2(x1), PolynomialOverZ2(x2), PolynomialOverZ2(v)

    def mulInverse(self, x):
        """
        :param x: x is the modulus
        :return: -1 if there is no inverse, or the inverse
        """
        if not isinstance(x, PolynomialOverZ2):
            raise TypeError
        self.__validityTest()
        x.__validityTest()
        if x.__expression == 1:
            raise exception.MultiplicativeInverseUseModulusOne
        r1, r2, r3 = self.extendGcd(x)
        if r3.__expression != 1:
            return PolynomialOverZ2(-1)
        return r2

    def equal(self, x):
        return self.__expression == x.__expression


def test():
    # while True:
    #     p1 = PolynomialOverZ2(random.randint(1, 0xffff))
    #     p2 = PolynomialOverZ2(random.randint(1, 0xffff))
    #     p3 = PolynomialOverZ2(random.randint(1, 0xffff))
    #     p4 = p1.fastMulWithMod(p2, p3)
    #     p5 = p1.mul(p2, p3)
    #     print(p1, p2, p3, p4, p5)
    #     assert p4.equal(p5)
    # exit(0)
    p = PolynomialOverZ2(0x2)
    print(p.mulInverse(PolynomialOverZ2(0x11b)))
    while True:
        p1 = PolynomialOverZ2(random.randint(1, 0xffff))
        p2 = PolynomialOverZ2(random.randint(1, 0xffff))
        p3 = p1 + p2
        p4 = p3 - p2
        p5 = p3 - p1
        print(p1, p2, p3, p4, p5)
        assert p1.equal(p4)
        assert p2.equal(p5)
        p3 = p1 * p2
        p4 = p3 / p1
        p5 = p3 / p2
        print(p1, p2, p3, p4, p5)
        assert p4.equal(p2)
        assert p5.equal(p1)
        p6 = p1 // p2
        p7 = p1 % p2
        assert p6.mul(p2).add(p7).equal(p1)
        p8, p9, p10 = p1.extendGcd(p2)
        print(p1, p2, p3, p4, p5)
        p11 = p8.mul(p2).add(p9.mul(p1))
        print(p11)
        assert p11.equal(p10)
        if int(p2) == 1:
            continue
        p12 = p1.mulInverse(p2)
        print(p12, p1, p2)
        if int(p12) != -1:
            assert p12.mul(p1, p2).equal(PolynomialOverZ2(1))


if __name__ == "__main__":
    test()
