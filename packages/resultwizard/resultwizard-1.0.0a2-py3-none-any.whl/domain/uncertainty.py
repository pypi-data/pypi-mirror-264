from domain.value import Value


class Uncertainty:
    """
    A named uncertainty value, e.g. a systematic uncertainty of ±0.1cm
    when measuring a length. In this case the uncertainty would be 0.1 and the name
    would be "systematic". As Uncertainties are always directly associated with a
    Result, we don't store the unit of the value here.

    We don't use the word "error" to distinguish between errors in our code,
    and uncertainties in the physical sense. In reality, these words might be used
    interchangeably.
    """

    def __init__(self, uncertainty: Value, name: str = ""):
        self.uncertainty = uncertainty
        self.name = name
