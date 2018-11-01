from CryptographyLib import util
from Experiment_5.__scaffold import decAndEnc_2
from Experiment_5.__scaffold import oracle_2, param_2


def MSBAttack_3(c, e, n, check=None):
    """
    this MSBAttack_3 only for n where the bit just next to msb is 0
    (i.e. if msb is ath bit, then the (a-1)th bit should be 0

    also, this method may not fit to other n and e, except
    n == 10972248137587377366511872502374418540148785271864664140224003976912394763519345894330351399072725587226569450675744223489916367725490099660444694424799368050354747903307229716596621313018741475082453227465782426508778695727856907406531408932372312410789803130093642493798583968796496712281799699858501519
    e = 113

    this is because that the algorithm is heuristic algorithm,
    so the strategy should be select specialized
    and use the oracle who check the bit next to msb

    :param c: the ciphertext
    :param n: the modulus
    :return: plaintext
    """

    def step2Exp(M: list, s: int, B: int, c0: int):
        minA, maxB = M[0][0], M[0][1]
        for i in M:
            minA = min(minA, i[0])
            maxB = max(maxB, i[1])
        k = (maxB * s - B)
        # ___
        k = (k // n) + (k % n > 0)
        r = (k + k)
        # ___
        found = False
        while not found:
            t1, t2 = (B + r * n), (2 * B - 1 + r * n)
            x, y = t1 // maxB + (t1 % maxB > 0), t2 // minA
            oldS = s
            for t in range(x, y + 1):
                c1 = c0 * util.fastModulePow(t, e, n)
                if oracle_2.MSBOracle(c1):
                    s = t
                    found = True
                    break
            r += 1
        return s, oldS

    # step 1: get c0=c(s0)^e where c0 is not oracle.MSBOracle(c0)
    # if c had been this conform, can skip this step
    B = 1 << (util.bitLen(n) - 2)
    M = [(B, 2 * B - 1)]
    c0, s0, s0r, s, oldS, it = 0, 0, 0, 0, 0, 1
    stepForStep2Iter = 1
    oldMLen, lastIntervalLen = 0, 0
    __stepForStepOne, __tForStepOne = 1, 1
    while True:
        c0 = c * util.fastModulePow(__tForStepOne, e, n) % n
        if util.binaryGCD(__tForStepOne, n) == 1 and oracle_2.MSBOracle(c0):
            s0, s = __tForStepOne, __tForStepOne
            # assert M[0][0] <= decAndEnc_2.dec(c0) <= M[0][1]
            # print(decAndEnc_2.dec(c0), check * s0 % n)
            # assert decAndEnc_2.dec(c0) == check * s0 % n
            break
        __stepForStepOne *= 2
        __tForStepOne += __stepForStepOne

    print(s, file=s0Output)
    print("s: ", s)

    __t, s0r = util.mulInverse(s0, n)
    assert __t
    # for i in M:
    #     print(i[0], i[1], check * s0 % n)
    #     assert i[0] <= check * s0 % n <= i[1]

    while True:
        if it == 1:
            oldS = s
            for t in range(n // (2 * B - 1) + (n % (2 * B - 1) > 0), n):
                c1 = c0 * util.fastModulePow(t, e, n) % n
                if oracle_2.MSBOracle(c1):
                    s = t
                    break
            print("case 1: ", s)
        elif len(M) <= 1:  # oldMLen:  # and len(M) < 100000000:
            s, oldS = step2Exp(M, s, B, c0)
            print("case 2: ", s)
        else:
            oldS = s
            for t in range(s + stepForStep2Iter, n):
                c1 = c0 * util.fastModulePow(t, e, n) % n
                if oracle_2.MSBOracle(c1):
                    s = t
                    break
            print("case 3: ", s)
        if oldS == s:
            # print("no new s, len(M): ", len(M))
            # print(M)
            # print([i[1] - i[0] for i in M])
            # print()
            # k = [(i[0] * s0r % n, i[1] * s0r % n) for i in M]
            # for i in M:
            #     if i[0] <= check * s0 % n <= i[1]:
            #         print(i, i[1] - i[0], param_2.n, (i[1] - i[0]) / param_2.n)
            #         print("in one interval")
            #         if i[1] - i[0] < 1000:
            #             print("Success")
            # for i in k:
            #     if i[0] == check or i[1] == check:
            #         print("Success", i)
            return False

        print(s, file=s0Output)
        print("s: ", s)

        nm = list()
        __tmpL = -1
        for i in M:
            # t1, t2 = i[0] * s - 2 * B + 1, i[1] * s - B
            # x, y = t1 // n, t2 // n + 1
            # for j in range(x, y + 1):
            #     t1 = max(i[0], ((B + j * n) // s))
            #     t2 = min(i[1], (2 * B - 1 + j * n) // s + 1)
            #     if t1 <= t2:
            #         __tmpL = t2 - t1
            #         nm.add((t1, t2))

            # ________
            t1, t2 = i[0] * s - 2 * B + 1 + 1, i[1] * s - B
            x = t1 // n + (t1 % n > 0)
            y = t2 // n
            print("rMin: ", x)
            print("rMax: ", y)
            for j in range(x, y + 1):
                q = B + j * n
                p = 2 * B - 1 + j * n - 1
                t1 = max(i[0], q // s + (q % s > 0))
                t2 = min(i[1], p // s)
                if t1 <= t2:
                    print("i[0]: ", i[0])
                    print("ss: ", (q // s + (q % s > 0)))
                    print("t1: ", t1)
                    print("t2: ", t2)
                    __tmpL = t2 - t1
                    nm.append((t1, t2))
            print("\n")
        print("\n\n")

        # oldMLen = len(M)
        # M = list(nm)
        # __
        M = nm
        # __

        print("len(M): ", len(M))
        print("tmpDiff: ", util.numberLen(
            lastIntervalLen, 10), util.numberLen(__tmpL, 10))
        print(__tmpL)
        print("step: ", stepForStep2Iter)
        print("it: ", it)
        print()

        if it == 1:
            lastIntervalLen = __tmpL
        elif util.numberLen(lastIntervalLen, 10) > util.numberLen(__tmpL, 10):
            lastIntervalLen = __tmpL
            stepForStep2Iter *= 10

        it = it + 1

        # included = False
        # for i in M:
        #     included = included or (i[0] <= check * s0 % n <= i[1])
        # assert included

        allNarrow = True
        for i in M:
            allNarrow = allNarrow and i[1] - i[0] < 1000
        if allNarrow:
            resFile = open("./1.txt", "w")
            cnt = 0
            for j in M:
                print([k * s0r % n for k in range(j[0], j[1] + 1)], file=resFile)
                cnt += j[1] - j[0] + 1
            print("cnt: ", cnt)
            resFile.close()
            return [[z*s0r % n for z in range(k[0], k[1]+1)] for k in M]


if __name__ == "__main__":
    p = 9086392988939546881642644416028815353560712803262924991123003293380576913539458318742322252357100876922002826340850685077586992022670823089714921783344391433736513473050947875637071265092890728312505146465783410786077486194754154890172381266273349351556374613078187758176044497241425480037950406531842887
    c = decAndEnc_2.enc(p)
    e, n = param_2.e, param_2.n
    assert c == 3361544169850847375839766338159774550418715118762659043831748746520007328793399836962640931008398205409865883137128937335377097931302109345319778124351260660721174397345649870406920629118944038730481189127811896846236622567950865918375524078084248080393016415328661875447855968054940749914481699889040462

    s0Output = open("./2.txt", "w")
    res = MSBAttack_3(c, e, n)
    s0Output.close()
    for o in res:
        for l in o:
            if util.fastModulePow(l, e, n) == c:
                assert l == p
                print("res is: ", l)
