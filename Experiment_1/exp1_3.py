import random
from CryptographyLib import util
from CryptographyLib import exception


def congruenceEquation(a, b, n):
    """
    ax=b(mod n)
    :return: list of the result, if list is empty, no solution
    """
    if n <= 0:
        raise exception.ModuleNotPositiveException
    if a == 0 and b == 0:
        ans = [0]
        for i in range(1, n - 1):
            ans.append(i)
        return ans
    a, b = a % n, b % n
    t = util.binaryGCD(a, n)
    if b // t != b / t:
        return []
    x, y, z = util.extendBinaryGCD(a, n)
    ans = [x * (b // z) % n]
    for i in range(1, z - 1):
        ans.append(ans[0] + i * n // z)
    return ans


if __name__ == "__main__":
    while True:
        a = random.randint(0, 1000)
        b = random.randint(0, 1000)
        n = random.randint(1, 1000)
        ans = congruenceEquation(a, b, n)
        print(a, b, end=": ")
        if len(ans) == 0:
            print("No Solution")
        else:
            print(ans)
        for i in ans:
            assert a * i % n == b % n
