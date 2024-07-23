"""Test currency conversion"""

import pytest

from cmem_plugin_currencies.exceptions import InvalidDateError, WrongCurrencyCodeError
from cmem_plugin_currencies.transform import (
    CurrenciesConverter,
    get_current_date,
)


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
    with pytest.raises(WrongCurrencyCodeError):
        # works not for 2024
        CurrenciesConverter(from_currency="EUR", to_currency="RUB", date="2024-01-01").transform(
            inputs=[["1"]]
        )
    # works for 2010
    CurrenciesConverter(from_currency="EUR", to_currency="RUB", date="2010-01-01").transform(
        inputs=[["1"]]
    )


def test_multi_inputs() -> None:
    """Test multiple inputs"""
    plugin = CurrenciesConverter()
    inputs = [
        ["1", "1", "1", "1"],
        ["EUR", "EUR", "EUR", "EUR"],
        ["2024-04-01", "2024-05-01", "2024-06-01", "2024-07-01"],
        ["EUR", "EUR", "EUR", "EUR"],
    ]
    transformed = plugin.transform(inputs=inputs)
    assert transformed == ["1.0", "1.0", "1.0", "1.0"]

    inputs = [
        ["1", "1", "1", "1"],
        ["EUR", "EUR", "EUR", "EUR"],
        ["2024-04-01", "2024-05-01", "2024-06-01", "2024-07-01"],
        ["USD", "CZK", "DKK", "GBP"],
    ]
    transformed = plugin.transform(inputs=inputs)
    assert transformed == ["1.0811", "25.14", "7.4588", "0.8479"]


def test_get_current_date() -> None:
    """Test get_current_date function"""
    date = get_current_date()
    ten = 10
    assert len(date) == ten


def test_date_validated() -> None:
    """Test date_validated function"""
    assert CurrenciesConverter.date_validated("2024-01-01") == "2024-01-01"
    with pytest.raises(InvalidDateError):
        CurrenciesConverter.date_validated("2024-01-32")
    with pytest.raises(InvalidDateError):
        CurrenciesConverter.date_validated("2024")
    with pytest.raises(InvalidDateError):
        CurrenciesConverter.date_validated("2024-01")
    with pytest.raises(InvalidDateError):
        CurrenciesConverter.date_validated("0000-00-00")
    with pytest.raises(InvalidDateError):
        CurrenciesConverter.date_validated("xxx")
    with pytest.raises(InvalidDateError):
        CurrenciesConverter.date_validated("1999-01-03")
    with pytest.raises(InvalidDateError):
        CurrenciesConverter.date_validated("9999-01-03")


def test_get_rate() -> None:
    """Test get_rate function"""
    plugin = CurrenciesConverter()
    rate = plugin.get_rate("USD", get_current_date())
    assert rate >= 0


def test_wrong_date() -> None:
    """Test wrong dates"""
    CurrenciesConverter(date="2024-01-01")
    with pytest.raises(InvalidDateError):
        CurrenciesConverter(date="WRONG").transform(inputs=[["1"]])
    with pytest.raises(InvalidDateError):
        CurrenciesConverter(date="24-01-01").transform(inputs=[["1"]])
    with pytest.raises(InvalidDateError):
        CurrenciesConverter(date="1000-01-01").transform(inputs=[["1"]])


def test_wrong_currency() -> None:
    """Test wrong currencies"""
    with pytest.raises(WrongCurrencyCodeError):
        CurrenciesConverter(date="2024-07-22", from_currency="TTT").transform(inputs=[["1"]])
    with pytest.raises(WrongCurrencyCodeError):
        CurrenciesConverter(date="2024-01-01", from_currency="WRONG_FROM").transform(inputs=[["1"]])
    with pytest.raises(WrongCurrencyCodeError):
        CurrenciesConverter(
            date="2024-01-01", to_currency="WRONG_TO", from_currency="WRONG_FROM"
        ).transform(inputs=[["1"]])
