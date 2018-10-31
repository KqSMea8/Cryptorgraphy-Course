from CryptographyLib import util

p = 3773962424821541352241554580988268890916921220416440428376206300245624162392148852086126725177658767541468375030763844899770584629924792632561434251432696043649395327187
q = 2907354897182427562197295231552018137414565442749272241125960796722557152453591693304764202855054262243050086425064711734138406514458837
n = p * q
phi = (p - 1) * (q - 1)
e = 113
d = util.mulInverse(e, phi)[1]
assert n == 10972248137587377366511872502374418540148785271864664140224003976912394763519345894330351399072725587226569450675744223489916367725490099660444694424799368050354747903307229716596621313018741475082453227465782426508778695727856907406531408932372312410789803130093642493798583968796496712281799699858501519

# p = 0
# q = 0
# e = 0
# d = 0
# n = 0
# phi = 0
# while True:
#     l = len(primerList.primerList)
#     p = primerList.primerList[random.randint(l // 2 + l // 3, l)]
#     q = primerList.primerList[random.randint(l // 3 + l / 2, l)]
#     if p == q:
#         continue
#     n = p * q
#     if (n >> (util.bitLen(n) - 2) & 1) == 1:
#         continue
#     phi = (p - 1) * (q - 1)
#     e = primerList.primerList[random.randint(0, 300)]
#     tmp = util.mulInverse(e, phi)
#     while not tmp[0]:
#         e = primerList.primerList[random.randint(0, 300)]
#         tmp = util.mulInverse(e, phi)
#     d = tmp[1]
#     break
# assert (d * e - 1) % phi == 0

if __name__ == "__main__":
    print("p: ", p)
    print("q: ", q)
    print("e: ", e)
    print("d: ", d)
    print("n: ", n)
    print("phi: ", phi)
    print("len(n): ", util.bitLen(n))
