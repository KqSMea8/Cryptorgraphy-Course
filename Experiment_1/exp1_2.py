import random
from CryptographyLib import util

if __name__ == "__main__":
    while True:
        a = random.randint(1, 10000)
        b = random.randint(1, 10000)
        x, y, z = util.extendBinaryGCD(a, b)
        print(a, b, x, y, z)
        assert a * x + b * y == z
