import random
from CryptographyLib import util


def getAllPairGCD(q):
    """
    assume that x[i] != x[j] (i!=j)
    :return: this list l where l[(len(x)-1)*i+j] is gcd(x[i], x[j])
    calculate
    gcd{X[0],X[1]X[2]X[3]...};
    gcd{X[1],X[0]X[2]X[3]...};
    gcd{X[2],X[0]X[1]X[3]...};
    etc.
    if gcd{X[0],X[1]X[2]X[3]...} != 1,
    then calculate gcd(X[i], X[i]) (i is 1....)
    """
    p = [i for i in q]
    if type(p) != list:
        raise TypeError
    n = util.increaseTo2Pow(len(p))
    for i in range(len(p), n):
        p.append(1)
    d = util.batchGCD(p)
    ans = []
    for i in range(len(q)):
        if d[i] == 1:
            ans.append([1 for j in range(len(q))])
        else:
            ans.append([util.binaryGCD(p[i], p[j]) for j in range(len(q))])
    for i in range(len(q)):
        ans[i][i] = q[i]
    return ans


if __name__ == "__main__":
    while True:
        l = []
        for i in range(random.randint(100, 1000)):
            l.append(random.randint(1, 1000))
        s = []
        for i in range(len(l)):
            tmp = []
            for j in range(len(l)):
                tmp.append(util.binaryGCD(l[i], l[j]))
            s.append(tmp)
        t = getAllPairGCD(l)
        assert len(t) == len(s)
        ist = False
        # trivial way for checking
        for i in range(len(s)):
            assert len(s[i]) == len(s)
            for j in range(len(s)):
                if t[i][j] != s[i][j]:
                    ist = True
                    break
        if ist:
            for i in range(len(s)):
                print(s[i])
                print(t[i])
                print()
            break
        else:
            continue
