"""Plugin exceptions."""


class WrongCurrencyCodeError(Exception):
    """Wrong Currency Code Error

    will be raised when the currency code is not available in the rates.
    """


class InvalidDateError(ValueError):
    """Invalid Date Error

    will be raised when the date is invalid or no data is available.
    """
