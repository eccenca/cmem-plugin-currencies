"""currency converter plugin module"""
import requests
from collections.abc import Sequence

from cmem_plugin_base.dataintegration.description import (
    Plugin,
    PluginParameter,
)
from cmem_plugin_base.dataintegration.plugins import TransformPlugin


@Plugin(
    label="Currency Converter",
    description="Converts Currency"
                " from one to another."
                " Please use point as decimal separator and currency identifier as Currencies (e.g. EUR)",
    documentation="""
This Converter allows you to convert currencies from one currency to another. 
""",
    parameters=[
        PluginParameter(
            name="to_currency",
            label="Target Currency",
            description="currency identifier (e.g. USD).",
            default_value=None,
        ),
        PluginParameter(
            name="from_currency",
            label="Source Currency",
            description="currency identifier (e.g. EUR).",
            default_value=None,
        ),
    ],
)
class CurrenciesConverter(TransformPlugin):
    """Currency Converter Plugin"""

    def __init__(self, to_currency: str, from_currency: str):
        self.to_currency = to_currency
        self.from_currency = from_currency

    def transform(self, amount: Sequence[float]) -> Sequence[float]:
        """Do the actual transformation of values"""
        result = []

        response = requests.get(
            f"https://api.frankfurter.app/latest?amount={amount}&from_currency={self.from_currency}&to_currency={self.to_currency}")
        result = response.json()['rates'][self.to_currency]
        return result
