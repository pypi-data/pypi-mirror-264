from pyNastran.f06.errors import FatalError

class FortranMarkerError(Exception):
    pass

class EmptyRecordError(SyntaxError):
    pass

class SortCodeError(RuntimeError):
    pass

class DeviceCodeError(SyntaxError):
    pass

class MultipleSolutionNotImplementedError(NotImplementedError):
    pass

class MixedVersionCard(RuntimeError):
    pass

class SixtyFourBitError(NotImplementedError):
    pass

class OverwriteTableError(RuntimeError):
    pass

class DoubleCardError(RuntimeError):
    pass

class EmptyCardError(RuntimeError):
    pass
