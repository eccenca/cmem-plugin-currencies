"""currency converter plugin module"""
from collections.abc import Sequence

import requests
from cmem_plugin_base.dataintegration.description import (
    Plugin,
    PluginParameter,
)
from cmem_plugin_base.dataintegration.plugins import TransformPlugin


@Plugin(
    label="Currency Converter",
    description="Converts currencies"
    " from one to another."
    " Please use currency identifier e.g. EUR",
    documentation="""
This converter plugin allows you to convert currencies from one currency to another.
""",
    parameters=[
        PluginParameter(
            name="to_currency",
            label="Target Currency",
            description="Enter the currency code you want to convert to (e.g.USD).",
        ),
        PluginParameter(
            name="from_currency",
            label="Source Currency",
            description="Enter the currency code you want to convert from (e.g. EUR).",
        ),
        PluginParameter(
            name="historic",
            label="Historic Rate",
            description="Set date (e.g.YYYY-MM-DD) to convert currencies based on historic rates.",
        ),
    ],
)
class CurrenciesConverter(TransformPlugin):
    """Currency Converter Plugin"""

    def __init__(self, to_currency: str, from_currency: str, historic: str):
        self.historic = historic

        """Currency Check"""
        base_url = "https://api.frankfurter.app/"
        response = requests.get(base_url + "currencies", timeout=10)

        if to_currency.upper() in response.json() and from_currency.upper() in response.json():
            self.to_currency = to_currency.upper()
            self.from_currency = from_currency.upper()

            """API access, Historic or latest Rate"""
            url = base_url + historic if len(historic) > 0 else base_url + "latest"

            params = {"from": self.from_currency, "to": self.to_currency}
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            self.exchange_rate = float(data["rates"][self.to_currency])
        else:
            self.to_currency = ""
            self.from_currency = ""

    def transform(self, inputs: Sequence[str]) -> Sequence[str]:
        """Do the actual transformation of values"""
        return [str(self.exchange_rate * float(_)) for _ in inputs]
