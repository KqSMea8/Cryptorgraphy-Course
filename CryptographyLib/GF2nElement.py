from CryptographyLib.PolynomialOverZ2 import *
from CryptographyLib.exception import *


class GF2nElement:
    def __init__(self, expression, modulus):
        if isinstance(expression, int):
            self.__expression = PolynomialOverZ2(expression)
        elif isinstance(expression, PolynomialOverZ2):
            self.__expression = expression
        else:
            raise TypeError
        if isinstance(modulus, int):
            self.__modulus = PolynomialOverZ2(modulus)
        elif isinstance(modulus, PolynomialOverZ2):
            self.__modulus = modulus
        else:
            raise TypeError
        self.__expression = self.__expression.mod(self.__modulus)

    def __int__(self):
        return int(self.__expression)

    def __add__(self, other):
        self.__validityTest(other)
        return GF2nElement(self.__expression.add(other.__expression, self.__modulus), self.__modulus)

    def __sub__(self, other):
        self.__validityTest(other)
        return GF2nElement(self.__expression.sub(other.__expression, self.__modulus), self.__modulus)

    def __mul__(self, other):
        self.__validityTest(other)
        return GF2nElement(self.__expression.mul(other.__expression, self.__modulus), self.__modulus)

    def __floordiv__(self, other):
        self.__validityTest(other)
        return GF2nElement(self.__expression.mul(other.__expression.mulInverse(self.__modulus), self.__modulus),
                           self.__modulus)

    def __truediv__(self, other):
        return self // other

    def __eq__(self, other):
        self.__validityTest(other)
        return self.__expression == other.__expression

    def __str__(self):
        return str(self.__expression)

    def __repr__(self):
        return str(self.__expression)

    def __validityTest(self, x):
        if not isinstance(x, GF2nElement):
            raise TypeError(type(x))
        if not self.__modulus.equal(x.__modulus):
            raise ElementNotInSameGF2nField

    def innerExpressionOfInt(self):
        return self.__int__()

    def innerExpressionOfPolynomial(self):
        return self.__expression


def GF2nElementFactory(modulus: int):
    return lambda expression: GF2nElement(expression, modulus)


def test():
    # while True:
    #     a1 = GF2nElement(random.randint(1, 0x11b - 1), 0x11b)
    #     a2 = GF2nElement(random.randint(1, 0x11b - 1), 0x11b)
    #     a3 = a1 + a2
    #     a4 = a3 - a1
    #     a5 = a3 - a2
    #     print(a1, a2, a3, a4, a5)
    #     assert a4 == a2, (a4, a2)
    #     assert a5 == a1, (a5, a1)
    #     a6 = a1 * a2
    #     a7 = a6 / a1
    #     a8 = a6 / a2
    #     print(a1, a2, a6, a7, a8)
    #     assert a7 == a2, (a7, a2)
    #     assert a8 == a1, (a8, a1)
    f1 = GF2nElementFactory(0x11b)
    f2 = GF2nElementFactory(0x1b)
    try:
        var = f1(0x1) == f2(0x1)
        assert False
    except Exception as e:
        print(e.__class__, "OK")
        assert True


if __name__ == "__main__":
    test()
