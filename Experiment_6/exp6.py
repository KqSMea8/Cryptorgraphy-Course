import random
import time

# import matplotlib.pyplot as plt

from CryptographyLib.EllipticCurveElement import EllipticCurveElementOverGF2n
from CryptographyLib.GF2nElement import GF2nElement


def elementOfECOverGF2n(paramA: int, paramB: int, modulus: int, n: int):
    """
    :param paramA: the EC function's paramA
    :param paramB: the EC function's paramB
    :param modulus: the GF2n's modulus
    :param n: the GF2n's n
    :return: the order of EC over GF2n
    """
    elements = []
    for i in range(n):
        for j in range(n):
            if EllipticCurveElementOverGF2n. \
                    isPointInGroup(GF2nElement(paramA, modulus),
                            GF2nElement(paramB, modulus),
                            GF2nElement(i, modulus),
                            GF2nElement(j, modulus)):
                elements.append((i, j))
    return elements


def isTheGroupCyclic(elements):
    ss = set()
    for i in elements:
        ss.clear()
        k = i
        isAll = True
        for _ in range(len(elements)):
            k = k + i
            if k in ss:
                isAll = False
                break
            ss.add(k)
        if isAll:
            continue
        else:
            return True, i
    return False, None


# def draw(elements):
#     x, y = [i[0] for i in elements], [i[1] for i in elements]
#     plt.figure(1)
#     plt.scatter(x, y, c='r', marker='o')
#     plt.show()


def main():
    def check(x: int, y: int, m: int) -> bool:
        k1, k2 = GF2nElement(x, m), GF2nElement(y, m)
        k3, k4 = GF2nElement(4, m), GF2nElement(27, m)
        return k3 * k1 * k1 * k1 + k4 * k2 * k2 != GF2nElement(0, m)

    # t1 = time.clock()
    while True:
        t1 = time.clock()
        a = random.randint(1, 0x10)
        b = random.randint(1, 0x10)
        modulus = 0x11b
        if not check(a, b, modulus):
            continue
        elements = elementOfECOverGF2n(a, b, modulus, 0xff)
        isC = isTheGroupCyclic(elements)
        print(
            "len:", len(elements), "(a, b):", (a, b), "isCyclic:", isC, "time:",
            time.clock() - t1
        )
    # print(elements)
    # print(isTheGroupCyclic(elements))
    # print(time.clock() - t1)
    # draw(elements)


if __name__ == "__main__":
    main()
