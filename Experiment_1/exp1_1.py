def binaryGCD(x, y):
    x, y = abs(x), abs(y)
    if x == 0 or y == 0:
        return x + y
    if x == y:
        return x
    cnt = 0
    # this cycle is O(N^2)(assume that N = max(lgx, lgy))
    while ((x & 1) | (y & 1)) == 0:
        cnt += 1
        x = x >> 1
        y = y >> 1
    # the y below is surely odd
    # when x-y, x and y are odd, so x will become even
    # so the x>>1 will be run at least every two cycles
    # so this cycle is O(N^2)
    while x != 0:
        while (x & 1) == 0:
            x = x >> 1
        if y > x:
            x, y = y, x
        x, y = x - y, y
    return y * (1 << cnt)


def GCD(x, y):
    while y != 0:
        x, y = y, x % y
    return x
