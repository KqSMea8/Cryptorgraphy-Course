import math
import random
import gmpy

from CryptographyLib import util


def pollardRoh(n, cntToFind=-1):
    """
    :param n: the n to decompose
    :param cntToFind: the cnt of factor to find,
    if not set, find as far as possible
    :return: the list of factor, the cnt <= cntToFind
    """
    x = random.randint(0, n - 1)
    y, k = x, 2
    ans = []
    for j in range(1, n + 1):
        x = (x * x - 1) % n
        d = util.binaryGCD(y - x, n)
        print(x, d)
        if d == n:
            return ans
        if d != 1:
            print(d)
            ans.append(d)
        if j == k:
            y, k = x, k * 2
        if len(ans) == cntToFind:
            return ans


def assumeOneIsSmall(n, limit):
    for i in range(2, limit):
        if n % i == 0:
            print(i)
            break


def assumePSubQIsSmall(n, limit):
    s = gmpy.mpz(n)
    x = gmpy.sqrt(s)
    for i in range(limit):
        a, b = s//(x+i), s % (x+i)
        print(a, b, x+i)
        if b == 0:
            print(x+i, s//(x+i), s % (x+i))
            break


if __name__ == "__main__":
    n = 8419248954524000439721779172023134688983838205866625782151550834434276874684863239544369195264071670152656061813873751842115416791829324879655667191724512456544905595733991629887800889255133717212624547817690492648616532902257249552981800714896543008295153051040335475732125114592095784407296265046992475467
    assumePSubQIsSmall(n, 1000)
    # 成功原因：两个素因子非常接近
