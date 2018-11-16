from CryptographyLib import PolynomialOverZ2 as pl
from CryptographyLib import util


def constructGF2n(n: int):
    for i in range(1 << n, 1 << (n + 1)):
        if util.isPolynomialIrreducibleOnGF2n(pl.PolynomialOverZ2(i)):
            return True, pl.PolynomialOverZ2(i)
    return False, pl.PolynomialOverZ2(0)


if __name__ == "__main__":
    print(constructGF2n(10))
