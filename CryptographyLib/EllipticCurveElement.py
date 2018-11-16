from CryptographyLib.GF2nElement import *
from CryptographyLib.pythonUtil import ClassProperty


class EllipticCurveElementOverZp:
    # TODO
    # all properties should be const

    @ClassProperty
    def IDENTITY(self):
        return EllipticCurveElementOverZp(0, 0, 0, 0, 0, True)

    def __init__(self, paramA: int, paramB: int, modulus: int, x: int, y: int, isIdentity=False):
        self.__paramA = paramA
        self.__paramB = paramB
        self.__modulus = modulus
        self.__x = x
        self.__y = y
        self.__isIdentity = isIdentity

    def __str__(self):
        if self.__isIdentity:
            return "IDENTITY"
        return str((self.__x, self.__y))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, EllipticCurveElementOverZp):
            raise TypeError
        return self.__paramA == other.__paramA and \
               self.__paramB == other.__paramB and \
               self.__modulus == other.__modulus and \
               self.__isIdentity == other.__isIdentity and \
               ((self.__isIdentity and other.__isIdentity) or
                self.__x == other.__x and self.__y == other.__y)

    # the object's hash should not change in its lifecycle
    def __hash__(self):
        return (self.__paramA + self.__paramB + self.__modulus + self.__x + self.__y) * (self.__isIdentity * 2 - 1)

    def __add__(self, n):
        self.__validityTest(n)
        if n.__isIdentity:
            return self
        elif self.__isIdentity:
            return n
        else:
            if self.__x == n.__x and (self.__y != n.__y or self.__y == n.__y == 0):
                return EllipticCurveElementOverZp.IDENTITY
            if n != self:
                t1 = util.mulInverse(n.__x - self.__x, self.__modulus)
                assert t1[0], t1
                t = t1[1] * (n.__y - self.__y) % self.__modulus
            else:
                t1 = util.mulInverse(2 * self.__y, self.__modulus)
                assert t1[0], t1
                t = (3 * self.__x ** 2 + self.__paramA) * t1[1] % self.__modulus
            x3 = (t ** 2 - self.__x - n.__x) % self.__modulus
            return EllipticCurveElementOverZp(self.__paramA, self.__paramB, self.__modulus, x3,
                                              (t * (self.__x - x3) - self.__y) % self.__modulus)

    def __mul__(self, n: int):
        if not isinstance(n, int):
            raise TypeError
        if n < 0:
            raise EllipticCurveMulByNegativeNumber
        ans = EllipticCurveElementOverZp.IDENTITY
        t = self
        while n:
            if n & 1:
                ans += t
            t = t + t
            n >>= 1
        return ans

    def __validityTest(self, x):
        if not isinstance(x, EllipticCurveElementOverZp):
            raise TypeError
        if x.__isIdentity or self.__isIdentity:
            return
        if not (self.__paramA == x.__paramA and
                self.__paramB == x.__paramB and
                self.__modulus == self.__modulus):
            raise ElementNotInSameEllipticCurveGroup


class EllipticCurveElementOverGF2n:
    @ClassProperty
    def IDENTITY(self):
        # for identity, it is no matter what the paraA and paramB, modulus is,
        # however, the GF2nElement not allow 0 as modulus, so don't use 0 as modulus
        return EllipticCurveElementOverGF2n(GF2nElement(0, 1), GF2nElement(0, 1),
                                            GF2nElement(0, 1), GF2nElement(0, 1),
                                            True)

    def __init__(self, paramA: GF2nElement, paramB: GF2nElement, x: GF2nElement, y: GF2nElement, isIdentity=False):
        if not EllipticCurveElementOverGF2n.isPointInGroup(paramA, paramB, x, y):
            raise EllipticCurveElementNotInGroup
        self.__paramA = paramA
        self.__paramB = paramB
        self.__x = x
        self.__y = y
        self.__isIdentity = isIdentity

    def innerExpression(self):
        return int(self.__x), int(self.__y)

    def __str__(self):
        if self.__isIdentity:
            return "IDENTITY"
        return str((self.__x, self.__y))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, EllipticCurveElementOverGF2n):
            raise TypeError
        elif self.__isIdentity and other.__isIdentity:
            return True
        elif self.__isIdentity != other.__isIdentity:
            return False
        else:
            return self.__paramA == other.__paramA and \
                   self.__paramB == other.__paramB and \
                   self.__isIdentity == other.__isIdentity and \
                   self.__x == other.__x and self.__y == other.__y

    # the object's hash should not change in its lifecycle
    def __hash__(self):
        return int(self.__paramA + self.__paramB + self.__x + self.__y) * (self.__isIdentity * 2 - 1)

    def __add__(self, other):
        self.__validityTest(other)
        if other.__isIdentity:
            return self
        elif self.__isIdentity:
            return other
        else:
            tmp1 = self.__x + self.__y
            tmp2 = other.__x + other.__y
            if tmp1 == other.__y or tmp2 == self.__y:
                return EllipticCurveElementOverGF2n.IDENTITY
            elif self == other:
                t = self.__x + self.__y // self.__x
            else:
                t = (self.__y + other.__y) // (self.__x + other.__x)
            x3 = t * t + t + self.__x + other.__x + self.__paramA
            assert isinstance(x3, GF2nElement), type(x3)
            y3 = t * (self.__x + x3) + x3 + self.__y
            assert isinstance(y3, GF2nElement), type(y3)
            return EllipticCurveElementOverGF2n(self.__paramA, self.__paramB, x3, y3)

    def __mul__(self, n: int):
        if not isinstance(n, int):
            return TypeError
        t, ans = self, self
        while n:
            if n & 1:
                ans = ans + t
            t = t + t
            n >>= 1
        return ans

    def __validityTest(self, x):
        if not isinstance(x, EllipticCurveElementOverGF2n):
            raise TypeError
        if x.__isIdentity or self.__isIdentity:
            return
        if not (self.__paramA == x.__paramA and
                self.__paramB == x.__paramB):
            raise ElementNotInSameEllipticCurveGroup

    @staticmethod
    def isPointInGroup(paramA: GF2nElement, paramB: GF2nElement, x: GF2nElement, y: GF2nElement) -> bool:
        t1 = y * y + x * y
        t2 = x * x * x + paramA * x * x + paramB
        assert isinstance(t1, GF2nElement), type(t1)
        assert isinstance(t2, GF2nElement), type(t2)
        return t1 == t2


class EllipticCurveElementFactory:
    @ClassProperty
    def OverZp(self):
        return "Zp"

    @ClassProperty
    def OverGF2n(self):
        return "GF2n"

    @staticmethod
    def getFactory(group: str, paramA: int, paramB: int, modulus: int):
        """
        if type is GF2n, then modulus is used as GF2n's modulus
        """
        if group == EllipticCurveElementFactory.OverGF2n:
            GFFactory = GF2nElementFactory(modulus)

            def makeOverGF2n(x: int, y: int, isIdentity=False):
                return EllipticCurveElementOverGF2n(GFFactory(paramA), GFFactory(paramB),
                                                    GFFactory(x), GFFactory(y), isIdentity)

            return makeOverGF2n
        elif group == EllipticCurveElementFactory.OverZp:
            def makeOverZp(x: int, y: int, isIdentity=False):
                return EllipticCurveElementOverZp(paramA, paramB, modulus, x, y, isIdentity)

            return makeOverZp
        else:
            raise EllipticCurveElementNotSupportSuchGroup


if __name__ == "__main__":
    # print((EllipticCurveElementOverZp.IDENTITY, EllipticCurveElementOverZp.IDENTITY))
    # f1 = EllipticCurveElementFactory.getFactory(EllipticCurveElementFactory.OverZp, 9, 17, 23)
    # g = f1(16, 5)
    # g = EllipticCurveElementOverZp(9, 17, 23, 16, 5)
    # k = g
    # s = set()
    # s.add(g)
    # i = 2
    # while True:
    #     k = g + k
    #     print(k, g * i)
    #     i += 1
    #     if k in s:
    #         break
    #     s.add(k)
    # print(s, len(s))
    f1 = EllipticCurveElementFactory.getFactory(EllipticCurveElementFactory.OverGF2n, 0x3, 0x1, 0x13)
    g = EllipticCurveElementOverGF2n(GF2nElement(0x3, 0x13), GF2nElement(0x1, 0x13),
                                     GF2nElement(0x6, 0x13), GF2nElement(0x8, 0x13))

    # g = f1(0x6, 0x8)
    s = set()
    k = g
    print(k)
    s.add(g)
    i = 1
    while True:
        k = k + g
        print(k, g * i)
        i += 1
        if k in s:
            break
        s.add(k)
    print(s, len(s))
    # f1 = EllipticCurveElementFactory.getFactory(EllipticCurveElementFactory.OverGF2n, 0x1, 0x2, 0x3)
    # f2 = EllipticCurveElementFactory.getFactory(EllipticCurveElementFactory.OverGF2n, 0x1, 0x2, 0x2)
    # try:
    #     f1(1, 1) == f2(1, 1)
    #     assert False
    # except Exception as e:
    #     print(e.__class__, "OK")
    #     assert True
    # f3 = EllipticCurveElementFactory.getFactory(EllipticCurveElementFactory.OverZp, 10, 20, 30)
    # f4 = EllipticCurveElementFactory.getFactory(EllipticCurveElementFactory.OverZp, 10, 20, 40)
    # try:
    #     f3(1, 1) == f4(1, 1)
    #     assert False
    # except Exception as e:
    #     print(e.__class__, "OK")
    #     assert True
