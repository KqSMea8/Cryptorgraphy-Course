import random
from CryptographyLib import util
from CryptographyLib import exception


# calculate x where x**a==b(mod n)
# my program can only solve when gcd(a, phi(n))==1 and n which has no same prime factors

# consider the proof process of RSA at CLRS and Euler theory, no matter whether N is composed with different
# primer factor, there always has d make ad+r*phi(n)=1, so try to find the phi(n) of N to get the solution.
# be careful that gcd(x, n) must equal to 1, or it is False
# if n is primer, then phi(n) can be resolve O(p) (p==bitLen(n)), so all the complexity is O(p^3)
# (the fastModulePow need p times multiple and every time need p^2 (this can use FFT to optimize))
# if n is not primer, I need O(p^2*2^p) to get phi(n), and all the complexity is O(p^2*2^p)

def extractRoot(a, b, n):
    """
    :return: (hadSolution, x) where x[i]**a = b (mod n)
    """
    if n <= 0:
        raise exception.ModuleNotPositiveException
    if a < 0:
        raise exception.ExponentialNegativeException
    if a == 0:
        return b % n == 1 or n == 1, 0
    if b == 0:
        return True, 0
    if n == 1:
        return True, 0
    # if n==2, then phi(n)==1, then can't use RSA decrypt process
    if n == 2:
        return True, b
    b, phiN = b % n, util.phiFunction(n)
    x, y, z = util.extendBinaryGCD(a, phiN)
    assert (a * x + y * phiN == z)
    if x < 0:
        x %= phiN
    print("log: ", a, b, n, phiN, x, y, z)
    if z == 1:
        tmp = util.fastModulePow(b, x, n)
        assert tmp == b ** x % n
        if util.binaryGCD(tmp, n) != 1:
            return False, 0
        else:
            return True, util.fastModulePow(b, x, n)
    else:
        return False, 0


if __name__ == "__main__":
    while True:
        a = random.randint(1, 1000)
        b = random.randint(1, 1000)
        n = random.randint(1, 1000)
        x, y = extractRoot(a, b, n)
        print("Factor decompose: ", end="")
        for i in range(2, n + 1):
            if util.isPrimer(i) and n // i == n / i:
                print(i, end=", ")
        print()
        if x:
            print(a, b, n, x, y, y ** a % n)
            assert y ** a % n == b % n
            assert util.fastModulePow(y, a, n) == b % n
