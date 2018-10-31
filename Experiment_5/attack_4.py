from libnum import invmod, len_in_bits
import random
from libnum.ranges import Ranges  # added recently

from Crypto.PublicKey import RSA


n = 10972248137587377366511872502374418540148785271864664140224003976912394763519345894330351399072725587226569450675744223489916367725490099660444694424799368050354747903307229716596621313018741475082453227465782426508778695727856907406531408932372312410789803130093642493798583968796496712281799699858501519
d = 5631773380354583073076890310953241374589641997948234691442409120893087577735593467886375054391310478399478125125603229755886277239632084614300633955654556786817784788248274546877315674362254129304308459246406346877843235105135704417348637151057823162045381160052474175152639616056251972879591357071022113
e = 113
nmid = len_in_bits(n)-2

curlen = open("./curlen.txt", "w")


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


def decrypt(c):
    return fastModulePow(c, d, n)


def encrypt(p):
    return fastModulePow(p, e, n)


C = 3017789975616512251879092405212748273666515547772310277822133780585497954458336240163893568990957364597785493071188299074839300943184743075686782276534358970820903778076171875
i2 = fastModulePow(invmod(2, n), e, n)


def oracle(c):
    m = decrypt(c)
    v = (m >> nmid) & 3
    print(hex(m))
    a = v >> 1
    b = v & 1
    return a, b


def oracle_lsb(ct):
    a, b = oracle(ct)
    c, d = oracle((i2 * ct) % n)
    assert (b == 1 and a == 0) or (b == 0)
    if d == 1 and b == 1:
        assert a != 1
    return (d == 1) and (b == 1)


rng = Ranges((0, n - 1))


t = 1
while True:
    print ("blinding: ", t)
    if oracle_lsb(encrypt(t)*C % n):
        C = encrypt(t)*C % n
        break
    t = random.randint(2, n-1)


assert oracle_lsb(C), "need blinding..."
print "Good"

div = 2
ntotal = 0
ngood = 0
while 1:
    ntotal += 1
    div %= n
    C2 = (fastModulePow(div, e, n) * C) % n
    if not oracle_lsb(C2):
        div += 1
        continue

    ngood += 1
    cur = Ranges()
    for ml, mr in rng._segments:
        print>>curlen, "ml, mr: ", ml, mr, mr-ml, len_in_bits(mr-ml)
        kl = ml * div / n
        kr = mr * div / n
        # ensure correct parity
        if kl % 2 == div % 2:
            kl += 1
        print >> curlen, kl, kr
        k = kl
        cnt = 0
        while k <= kr:
            l = k * n / div
            r = (k + 1) * n / div
            cur = cur | Ranges((l, r))
            k += 2
            cnt += 1
        print >> curlen, "cnt: ", cnt, cnt-(kl-kr)

    # print("len(cur): ", len(cur._segments), file="curlen")
    print >> curlen, "len(cur): ", len(cur._segments), "len(rng): ", len(rng._segments)

    rng = rng & cur
    
    print >> curlen, "len(newRng): ", len(rng._segments), "\n\n"

    print "#%d/%d" % (ngood, ntotal), "good", div, "unknown bits:", len_in_bits(
        rng.len), "num segments", len(rng._segments)

    if rng.len <= 100:
        print "Few candidates left, breaking"
        break

    # heuristic to keep fewer intervals for M
    if len(rng._segments) <= 10:
        div = 2*div
    else:
        div = div + (div / 2) + (div / 4)

M = 35*t%n
print "Message in the %d candidates left?" % rng.len, M in rng
curlen.close()
