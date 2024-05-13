"""Test currency conversion"""
from cmem_plugin_currencies.currencies import CurrenciesConverter


def test_init() -> None:
    """Test Initialization"""
    plugin = CurrenciesConverter(from_currency="EUR", to_currency="USD", historic="")
    eur_values = ["1", "2"]
    usd_values = plugin.transform(inputs=eur_values)
    assert len(usd_values) == len(eur_values)
    for eur_value, usd_value in zip(eur_values, usd_values, strict=True):
        # assuming that 1 EUR is 1.xx USD
        assert float(eur_value) < float(usd_value)
