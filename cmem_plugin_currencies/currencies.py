"""currency converter plugin module"""

import re
from collections.abc import Sequence
from datetime import UTC, datetime
from http.client import NOT_FOUND

import requests
from cmem_plugin_base.dataintegration.description import (
    Plugin,
    PluginParameter,
)
from cmem_plugin_base.dataintegration.plugins import TransformPlugin

import cmem_plugin_currencies.exceptions as e

MESSAGE_WRONG_DATE = "Date is not valid. Please use this format: YYYY-MM-DD"
MESSAGE_NO_DATA_FOR_DATE = "No data available for this date."
MESSAGE_CURRENCY_NOT_AVAILABLE = "Currency is not available for this date."


def get_current_date() -> str:
    """Get current date in ISO 8601 format"""
    return datetime.now(tz=UTC).strftime("%Y-%m-%d")


@Plugin(
    label="Currency Converter",
    description="Converts currencies values with current and historical exchange rates",
    documentation="""
This converter plugin allows you to convert currencies from one currency to another.
""",
    parameters=[
        PluginParameter(
            name="to_currency",
            label="Target Currency",
            description="Enter the currency code you want to convert to (e.g.USD).",
            default_value="EUR",
        ),
        PluginParameter(
            name="from_currency",
            label="Source Currency",
            description="Enter the currency code you want to convert from (e.g. EUR).",
            default_value="USD",
        ),
        PluginParameter(
            name="date",
            label="Date",
            description="Set date (e.g.YYYY-MM-DD) to convert currencies based on historic rates.",
            default_value=get_current_date(),
        ),
    ],
)
class CurrenciesConverter(TransformPlugin):
    """Currency Converter Plugin"""

    BASE_URL = "https://api.frankfurter.app/"
    rates: dict[str, float]
    currencies: list[str]

    def __init__(
        self, to_currency: str = "EUR", from_currency: str = "USD", date: str = get_current_date()
    ):
        self.date = date
        self.to_currency = to_currency.upper()
        self.from_currency = from_currency.upper()
        self.check_parameters()

    def check_parameters(self) -> None:
        """Check validity of parameters"""
        # syntactic date check
        match = re.match(r"^\d{4}-([0][1-9]|1[0-2])-([0][1-9]|[1-2]\d|3[01])$", self.date)
        if match is None:
            raise e.InvalidDateError(MESSAGE_WRONG_DATE)
        # data for date check
        request = requests.get(self.BASE_URL + self.date, timeout=10)
        if request.status_code == NOT_FOUND:
            raise e.InvalidDateError(MESSAGE_NO_DATA_FOR_DATE)
        # prepare a list of currencies and rates
        self.rates = request.json()["rates"]
        self.currencies = list(self.rates)
        self.currencies.append("EUR")
        # check requested currencies against list
        if self.from_currency not in self.currencies:
            raise e.WrongCurrencyCodeError(
                f"{MESSAGE_CURRENCY_NOT_AVAILABLE}: {self.from_currency}"
            )
        if self.to_currency not in self.currencies:
            raise e.WrongCurrencyCodeError(f"{MESSAGE_CURRENCY_NOT_AVAILABLE}: {self.to_currency}")

    def exchange(self, value: float, from_currency: str, to_currency: str) -> float:
        """Convert value from one currency to another"""
        # convert to base currency (EUR) except if coming from EUR already
        value_in_eur = value / self.rates[from_currency] if from_currency != "EUR" else value
        # convert to target currency except if target currency is EUR
        return value_in_eur * self.rates[to_currency] if to_currency != "EUR" else value_in_eur

    def transform(self, inputs: Sequence[Sequence[str]]) -> Sequence[str]:
        """Do the actual transformation of values"""
        return [
            str(
                self.exchange(
                    value=float(_), from_currency=self.from_currency, to_currency=self.to_currency
                )
            )
            for _ in inputs[0]
        ]
