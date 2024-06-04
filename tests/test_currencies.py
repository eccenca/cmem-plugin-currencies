"""Test currency conversion"""

import pytest

from cmem_plugin_currencies.currencies import (
    MESSAGE_CURRENCY_NOT_AVAILABLE,
    MESSAGE_NO_DATA_FOR_DATE,
    MESSAGE_WRONG_DATE,
    CurrenciesConverter,
    get_current_date,
)
from cmem_plugin_currencies.exceptions import InvalidDateError, WrongCurrencyCodeError


def test_init() -> None:
    """Test Initialization"""
    plugin_to_usd = CurrenciesConverter(from_currency="EUR", to_currency="USD")
    eur_values = ["1", "2"]
    usd_values = plugin_to_usd.transform(inputs=[eur_values])
    assert len(usd_values) == len(eur_values)
    for eur_value, usd_value in zip(eur_values, usd_values, strict=True):
        # assuming that 1 EUR is 1.xx USD
        assert float(eur_value) < float(usd_value)
    plugin_to_eur = CurrenciesConverter(from_currency="USD", to_currency="EUR")
    new_eur_values = plugin_to_eur.transform([usd_values])
    for eur_value, new_eur_value in zip(eur_values, new_eur_values, strict=True):
        # assuming that old and new values are the same
        assert float(eur_value) == float(new_eur_value)


def test_rubel() -> None:
    """Test Rubel behaviour"""
    with pytest.raises(WrongCurrencyCodeError, match=f"{MESSAGE_CURRENCY_NOT_AVAILABLE}: RUB"):
        # works not for 2024
        CurrenciesConverter(from_currency="EUR", to_currency="RUB", date="2024-01-01")
    # works for 2010
    CurrenciesConverter(from_currency="EUR", to_currency="RUB", date="2010-01-01")


def test_get_current_date() -> None:
    """Test get_current_date function"""
    date = get_current_date()
    ten = 10
    assert len(date) == ten


def test_wrong_date() -> None:
    """Test wrong dates"""
    CurrenciesConverter(date="2024-01-01")
    with pytest.raises(InvalidDateError, match=MESSAGE_WRONG_DATE):
        CurrenciesConverter(date="WRONG")
    with pytest.raises(InvalidDateError, match=MESSAGE_WRONG_DATE):
        CurrenciesConverter(date="24-01-01")
    with pytest.raises(InvalidDateError, match=MESSAGE_NO_DATA_FOR_DATE):
        CurrenciesConverter(date="1000-01-01")


def test_wrong_currency() -> None:
    """Test wrong currencies"""
    with pytest.raises(
        WrongCurrencyCodeError, match=f"{MESSAGE_CURRENCY_NOT_AVAILABLE}: WRONG_FROM"
    ):
        CurrenciesConverter(date="2024-01-01", from_currency="WRONG_FROM")
    with pytest.raises(WrongCurrencyCodeError, match=f"{MESSAGE_CURRENCY_NOT_AVAILABLE}: WRONG_TO"):
        CurrenciesConverter(date="2024-01-01", to_currency="WRONG_TO")
    with pytest.raises(
        WrongCurrencyCodeError, match=f"{MESSAGE_CURRENCY_NOT_AVAILABLE}: WRONG_FROM"
    ):
        CurrenciesConverter(date="2024-01-01", to_currency="WRONG_TO", from_currency="WRONG_FROM")
