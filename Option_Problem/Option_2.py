from CryptographyLib import Polynomial as pl
from CryptographyLib import util


def constructGF2n(n: int):
    for i in range(1 << n, 1 << (n + 1)):
        if util.isPolynomialIrreducibleOnGF2n(pl.Polynomial(i)):
            return True, pl.Polynomial(i)
    return False, pl.Polynomial(0)
