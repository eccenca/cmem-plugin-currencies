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
                " Please use point as decimal separator "
                " and currency identifier as Currencies (e.g. EUR)",
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

    def transform(self, amount: float) -> float:
        """Do the actual transformation of values"""

        base_url = "https://api.frankfurter.app/latest"
        params = {"amount": amount, "from": self.from_currency, "to": self.to_currency}
        response = requests.get(base_url, params=params)
        data = response.json()
        exchange_rate = data["rates"][self.to_currency]
        converted_amount = amount*exchange_rate

        return converted_amount
