import time

import matplotlib.pyplot as plt

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


def draw(elements):
    x, y = [i[0] for i in elements], [i[1] for i in elements]
    plt.figure(1)
    plt.scatter(x, y, c='r', marker='o')
    plt.show()


if __name__ == "__main__":
    t1 = time.clock()
    elements = elementOfECOverGF2n(0x11, 0x12, 0x11b, 0xff)
    print(len(elements))
    print(elements)
    print(isTheGroupCyclic(elements))
    print(time.clock() - t1)
    draw(elements)
