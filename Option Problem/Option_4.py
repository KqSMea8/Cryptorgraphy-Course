from functools import reduce
from CryptographyLib import util


def enumBitIndex(c, m, bitNum):
    """
    enum the bitNum bits' distribution
    for example, if bitNum==2, then will enum 0b11, 0b101, 0b1001, and so on
    :param c: the ciphertext
    :param bitNum: the number of bit
    :return: (isSuccess, privateKey)
    """

    def bitListToNum(l: list):
        return reduce(lambda x, y: x * 2 + y, l)

    def inner(bitNumToPlace, bitNumForPlace, bitPattern: list):
        assert bitNumForPlace >= bitNumToPlace
        if bitNumToPlace == 1:
            yield bitListToNum(bitPattern + [0] * (bitNumForPlace - 1) + [1])
            return
        if bitNumToPlace == bitNumForPlace:
            yield bitListToNum(bitPattern + [1] * bitNumToPlace)
            return
        bitPattern.append(0)
        for j in inner(bitNumToPlace, bitNumForPlace - 1, bitPattern):
            yield j
        bitPattern[-1] = 1
        for j in inner(bitNumToPlace - 1, bitNumForPlace - 1, bitPattern):
            yield j
        bitPattern.pop()
        return

    nl = util.bitLen(n)
    bitNum = min(bitNum, nl)
    for i in inner(bitNum, nl, []):
        if util.fastModulePow(c, i, n) == m:
            return True, i
    return False, 0


def brute(n, e):
    assert n >= 0 and e >= 0
    if e == 1:
        return 1
    m = 2
    c = util.fastModulePow(m, e, n)
    s = enumBitIndex(c, m, 2)
    if s[0]:
        return s[1]
    for i in range(3, n, 2):
        if m == util.fastModulePow(c, i, n):
            return i


if __name__ == "__main__":
    n = 33608051123287760315508423639768587307044110783252538766412788814888567164438282747809126528707329215122915093543085008547092423658991866313471837522758159
    e = 14058695417015334071588010346586749790539913287499707802938898719199384604316115908373997739604466972535533733290829894940306314501336291780396644520926473
    print(brute(n, e))
