from CryptographyLib import util
from Experiment_5 import param_2


def MSBOracle(c):
    d = param_2.d
    n = param_2.n
    s = util.fastModulePow(c, d, n)
    return s >> (util.bitLen(n) - 2) & 1


def LSBOracle(c):
    d = param_2.d
    n = param_2.n
    s = util.fastModulePow(c, d, n)
    return s & 1
