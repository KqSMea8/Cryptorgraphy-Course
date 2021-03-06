import math
import random
from math import floor

from CryptographyLib import PolynomialOverZ2 as pl
from CryptographyLib import exception


def binaryGCD(x, y):
    x, y = abs(x), abs(y)
    if x == 0 or y == 0:
        return x + y
    if x == y:
        return x
    cnt = 0
    # this cycle is O(N^2)(assume that N = max(lgx, lgy))
    while ((x & 1) | (y & 1)) == 0:
        cnt += 1
        x = x >> 1
        y = y >> 1
    # the y below is surely odd
    # when x-y, x and y are odd, so x will become even
    # so the x>>1 will be run at least every two cycles
    # so this cycle is O(N^2)
    while x != 0:
        while (x & 1) == 0:
            x = x >> 1
        if y > x:
            x, y = y, x
        x, y = x - y, y
    return y * (1 << cnt)


def GCD(x, y):
    while y != 0:
        x, y = y, x % y
    return x


def batchGCD(x):
    """
    :param x: the list to calculate batch gcd, len(x) must be 2**n
    :return: the list of gcd{X[0],X[1]X[2]X[3]...}, gcd{X[1],X[0]X[2]X[3]...}, gcd{X[2],X[0]X[1]X[3]...}...
    """

    def productTree(a):
        ans = []
        __d = a
        while True:
            ans.append(__d)
            if len(__d) == 1:
                break
            # global __d
            __d = [__d[2 * i] * __d[2 * i + 1] for i in range(len(__d) // 2)]
        ans.append(__d)
        return ans

    if type(x) != list:
        raise TypeError
    t = len(x)
    if t == 0:
        return []
    if t == 1:
        return [x[0]]
    while t != 1:
        if t & 1 == 1:
            raise exception.BatchGCDLenIllegal
        t >>= 1
    p = productTree(x)
    d = p.pop()
    while p:
        k = p.pop()
        d = [d[floor(i / 2)] % k[i] ** 2 for i in range(len(k))]
    return [binaryGCD(r // n, n) for r, n in zip(d, x)]


def extendBinaryGCD(a, b):
    """Extended binary GCD.
    Given input a, b the function returns s, t, d
    such that gcd(a,b) = d = as + bt."""
    if a == 0:
        return 0, 1, b
    if b == 0:
        return 1, 0, a
    if a == b:
        return 1, 0, a
    u, v, s, t, r = 1, 0, 0, 1, 0
    while (a % 2 == 0) and (b % 2 == 0):
        a, b, r = a // 2, b // 2, r + 1
    alpha, beta = a, b
    #
    # from here on we maintain a = u * alpha + v * beta
    # and b = s * alpha + t * beta
    #
    while a % 2 == 0:
        # v is always even
        a = a // 2
        if (u % 2 == 0) and (v % 2 == 0):
            u, v = u // 2, v // 2
        else:
            u, v = (u + beta) // 2, (v - alpha) // 2
    while a != b:
        if b % 2 == 0:
            b = b // 2
            #
            # Commentary: note that here, since b is even,
            # (i) if s, t are both odd then so are alpha, beta
            # (ii) if s is odd and t even then alpha must be even, so beta is odd
            # (iii) if t is odd and s even then beta must be even, so alpha is odd
            # so for each of (i), (ii) and (iii) s + beta and t - alpha are even
            #
            if (s % 2 == 0) and (t % 2 == 0):
                s, t = s // 2, t // 2
            else:
                s, t = (s + beta) // 2, (t - alpha) // 2
        elif b < a:
            a, b, u, v, s, t = b, a, s, t, u, v
        else:
            b, s, t = b - a, s - u, t - v
    return s, t, (2 ** r) * a


def fastModulePow(x, y, n):
    """
    :return: x**y mod n
    """
    if y == 0:
        return 1 % n
    ans, x = 1 % n, x % n
    while y != 0:
        if (y & 1) == 1:
            ans = x * ans % n
        x, y = x * x % n, y // 2
    return ans


def isPrimer(n: int):
    if n % 2 == 0 or n == 1:
        return n == 2
    r, s = 0, n - 1
    while s % 2 == 0:
        r, s = r + 1, s // 2
    for _ in range(10):
        a = random.randrange(2, n)
        x = fastModulePow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = fastModulePow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def phiFunction(x):
    if x <= 0:
        raise exception.PhiParamNegative
    if isPrimer(x):
        return x - 1
    else:
        ans = x
        for i in range(2, x + 1):
            if isPrimer(i) and x // i == x / i:
                ans -= ans // i
        return ans


def bitLen(x):
    ans = 0
    while x:
        ans += 1
        x >>= 1
    return ans


def numberLen(x: int, base: int) -> int:
    x = abs(x)
    ans = 0
    while x:
        x //= base
        ans += 1
    return ans


def increaseTo2Pow(x):
    k = 1 << bitLen(x)
    if k >> 1 == x:
        return x
    else:
        return k


def isPolynomialIrreducibleOnGF2n(p):
    """
    the calculate on polynomial's coefficient is under mod 2
    """
    if not isinstance(p, pl.PolynomialOverZ2):
        raise TypeError
    for i in range(2, int(p)):
        if not p.gcd(pl.PolynomialOverZ2(i)).equal(pl.PolynomialOverZ2(1)):
            return False
    return True


def mulInverse(a, n):
    """
    calculate b where ab=1(mod n)
    :return (doesExist, answer)
    """
    s, t, d = extendBinaryGCD(a % n, n)
    return d == 1, s % n


if __name__ == "__main__":
    # test isPrimer
    def trivialIsPrimer(n):
        if n & 1 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 2, 2):
            if n % i == 0:
                return False
        return True


    def trivialDecompose(n, toFind=-1):
        ans = []
        for j in range(2, int(math.sqrt(n)) + 1):
            if n % j == 0:
                ans.append(j)
            if len(ans) == toFind:
                return ans
        return ans


    # while True:
    #     a = random.randint(10, 10000000)
    #     b = random.randint(20, 33333333333) + a
    #     x, y = mulInverse(a, b)
    #     print(x, y)
    #     if x:
    #         assert a * y % b == 1
    assert numberLen(100, 10) == 3
    assert numberLen(12345678, 10) == 8
    assert numberLen(0, 10) == 0
    assert numberLen(1, 10) == 1
    assert isPolynomialIrreducibleOnGF2n(pl.PolynomialOverZ2(0x13))
    assert not isPolynomialIrreducibleOnGF2n(pl.PolynomialOverZ2(0x14))
    assert isPolynomialIrreducibleOnGF2n(pl.PolynomialOverZ2(0x11b))
    assert False
