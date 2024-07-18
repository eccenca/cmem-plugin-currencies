"""Test eurofxref module."""

from cmem_plugin_currencies.eurofxref import get_rates_from_api, get_rates_from_dump

TEST_DATE = "2024-07-12"
ROWS_ON_2024_07_12 = 6538
USD_RATE_ON_2024_07_12 = 1.089


def test_csv_parsing() -> None:
    """Test CSV parsing."""
    rates = get_rates_from_dump()
    rates[TEST_DATE]["USD"] = USD_RATE_ON_2024_07_12
    assert len(rates) >= ROWS_ON_2024_07_12
    assert get_rates_from_dump()[TEST_DATE]["USD"] == USD_RATE_ON_2024_07_12


def test_api() -> None:
    """Test API Requests"""
    rates = get_rates_from_api(date=TEST_DATE)
    assert rates["USD"] == USD_RATE_ON_2024_07_12
