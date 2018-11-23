class ExponentialNegativeException(Exception):
    pass


class ModuleNotPositiveException(Exception):
    pass


# when calculate multiplicative inverse, use one as modulus
class MultiplicativeInverseUseModulusOne(Exception):
    pass


class BatchGCDLenIllegal(Exception):
    pass


class PhiParamNegative(Exception):
    pass


class NegativePolynomialExpression(Exception):
    pass


class AESEncryptParamException(Exception):
    pass


class EllipticCurveCoordinateIllegal(Exception):
    pass


class ElementNotInSameGF2nField(Exception):
    pass


class ElementNotInSameEllipticCurveGroup(Exception):
    pass


class EllipticCurveMulByNegativeNumber(Exception):
    pass


class EllipticCurveElementNotInGroup(Exception):
    pass


class EllipticCurveElementNotSupportSuchGroup(Exception):
    pass


class EllipticCurveParamIllegal(Exception):
    pass
