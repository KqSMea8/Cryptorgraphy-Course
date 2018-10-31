import gmpy
from imp import reload

from CryptographyLib import util
from Option_Problem.__scaffold import param


def wienersAttack(e, n, debugInfo=None):
    def continuedFractionExpansion(x, y):
        a, r = x // y, x % y
        yield a
        while r:
            x, y = y, r
            a, r = x // y, x % y
            yield a

    def convergence(it):
        if it == 0:
            MT[0] = FT[0]
            DT[0] = 1
        elif it == 1:
            MT[1] = FT[1] * FT[0] + 1
            DT[1] = FT[1]
        else:
            MT[it & 1] = MT[(it - 1) & 1] * FT[it & 1] + MT[(it - 2) & 1]
            DT[it & 1] = DT[(it - 1) & 1] * FT[it & 1] + DT[(it - 2) & 1]
        return MT[it & 1], DT[it & 1]

    def checkAndDecompose(k, d):
        t = e * d - 1
        if t % k != 0:
            return False, 0, 0
        phi = t // k
        pAq = n - (phi - 1)
        pSqP2 = pAq ** 2 - 4 * n
        if gmpy.is_square(gmpy.mpz(pSqP2)):
            pSq = int(gmpy.sqrt(pSqP2).digits())
            p, q = (pSq + pAq) // 2, (pAq - pSq) // 2
            # print("check: ", p, q, p * q, n)
            assert p * q == n
            return True, p, q
        return False, 0, 0

    FT = [0, 0]  # fraction tuple
    MT = [0, 0]  # molecule tuple
    DT = [0, 0]  # denominator tuple
    # only contain two element
    # when index is even, the first is new fraction
    # when index is odd, the second one is new fraction
    __t1, __t2 = 0, 0
    for i, j in enumerate(continuedFractionExpansion(e, n)):
        FT[i & 1] = j
        k, d = convergence(i)
        __t1, __t2 = k, d
        print("log: ", k, d, file=logFile)
        assert d != 0
        if k == 0:
            continue
        ok, p, q = checkAndDecompose(k, d)
        if ok:
            return d, p, q
    assert (__t1, __t2) == (
        e // util.binaryGCD(e, n), n // util.binaryGCD(e, n))
    return 0, 0, 0


if __name__ == "__main__":
    logFile = open("./log.txt", "w")
    e = 14058695417015334071588010346586749790539913287499707802938898719199384604316115908373997739604466972535533733290829894940306314501336291780396644520926473
    n = 33608051123287760315508423639768587307044110783252538766412788814888567164438282747809126528707329215122915093543085008547092423658991866313471837522758159
    a, b, c = wienersAttack(e, n)
    print("d: ", a)
    print("p: ", b)
    print("q: ", c)
    logFile.close()

    # while True:
    #     reload(param)
    #     n, e, d = param.n, param.e, param.d
    #     p, q = param.p, param.q
    #     a, b, c = wienersAttack(e, n)
    #     print(a)
    #     print(b)
    #     print(c)
    #     print()
    #     print(d)
    #     print(p)
    #     print(q)
    #     if a == 0:
    #         continue
    #     assert a == d and {p, q} == {b, c}
