from CryptographyLib import util
from Experiment_5 import param_2


def dec(c):
    d = param_2.d
    n = param_2.n
    return util.fastModulePow(c, d, n)


def enc(p):
    e = param_2.e
    n = param_2.n
    return util.fastModulePow(p, e, n)


if __name__ == "__main__":
    k = util.bitLen(param_2.n)
    s = (1 << (k - 1))
    w = enc((s + 45) % param_2.n)
