"""additional tests"""
from cmem_plugin_currencies.exceptions import WrongCurrencyCodeError


def test_wrong_currency_exception() -> None:
    """Test the custom exception"""
    ttt = WrongCurrencyCodeError(currency="USD", date="2024-07-25")
    assert str(ttt) == "No rate for USD (2024-07-25) available."
