__all__ = ["YarNumBaseError", "NonIntegerInputError", "InvalidFormError"]


class YarNumBaseError(Exception):
    pass


class NonIntegerInputError(YarNumBaseError):
    def __init__(self, v: object) -> None:
        super().__init__(f"Provided value is not a valid integer: {str(v)}")


class InvalidFormError(YarNumBaseError):
    def __init__(self, v: object) -> None:
        super().__init__(f"Provided inflection form is not valid: {str(v)}")


class RangeError(YarNumBaseError):
    def __init__(self, n, max_len: int) -> None:
        super().__init__(
            f"Provided number is too large with {len(n)} out of {max_len} digits."
        )


class InternalDataError(YarNumBaseError):
    def __init__(self) -> None:
        super().__init__(f"Numeral in the requested form not found in internal data")
