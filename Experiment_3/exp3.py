from functools import reduce
from pprint import pprint

from CryptographyLib import Polynomial as pl


def SBoxGen():
    def numToBitArray(x):
        return [(x >> i) & 1 for i in range(7, -1, -1)]

    def bitArrayToNum(x):
        return reduce(lambda t1, t2: t1 * 2 + t2, x)

    ls = 16
    p = pl.Polynomial(0x11b)
    t = [[pl.Polynomial(i * 16 + j).mulInverse(p).expression for j in range(ls)] for i in range(ls)]
    t[0][0] = 0
    for i in range(ls):
        for j in range(ls):
            tmp = t[i][j]
            k = numToBitArray(tmp)
            t[i][j] = bitArrayToNum([reduce(lambda x, y: x ^ y, [k[(i + j) % 8] for j in range(5)])
                                     for i in range(8)])
            t[i][j] ^= 0x63
    return t


if __name__ == "__main__":
    pprint(SBoxGen())
