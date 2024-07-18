"""currency converter plugin module"""

from collections.abc import Generator, Sequence
from datetime import UTC, datetime

from cmem_plugin_base.dataintegration.description import (
    Plugin,
    PluginParameter,
)
from cmem_plugin_base.dataintegration.plugins import TransformPlugin

import cmem_plugin_currencies.exceptions as e
from cmem_plugin_currencies.eurofxref import get_rates_from_api, get_rates_from_dump


def get_current_date() -> str:
    """Get current date in ISO 8601 format"""
    return datetime.now(tz=UTC).strftime("%Y-%m-%d")


@Plugin(
    label="Convert currency values",
    plugin_id="cmem_plugin_currencies-transform",
    description="Converts currencies values with current and historical exchange rates",
    documentation="""
This converter plugin allows you to convert currencies from one currency to another.
""",
    parameters=[
        PluginParameter(
            name="from_currency",
            label="1. Source Currency",
            description="The currency code you want to convert from (e.g. USD).",
            default_value="USD",
        ),
        PluginParameter(
            name="date",
            label="2. Date",
            description="Set date (e.g.YYYY-MM-DD) to convert currencies based on historic rates.",
            default_value=get_current_date(),
        ),
        PluginParameter(
            name="to_currency",
            label="3. Target Currency",
            description="Enter the currency code you want to convert to (e.g.USD).",
            default_value="EUR",
        ),
    ],
)
class CurrenciesConverter(TransformPlugin):
    """Currency Converter Plugin"""

    historic_rates: dict[str, dict[str, float]] | None

    def __init__(
        self, from_currency: str = "USD", date: str = get_current_date(), to_currency: str = "EUR"
    ):
        self.historic_rates = None
        self.date = self.date_validated(date)
        self.to_currency = to_currency.upper()
        self.from_currency = from_currency.upper()

    @staticmethod
    def date_validated(date: str) -> str:
        """Validate a date string."""
        try:
            parsed_date = datetime.fromisoformat(date).strftime("%Y-%m-%d")
        except ValueError as error:
            raise e.InvalidDateError(error) from error
        if parsed_date < "1999-01-04":
            raise e.InvalidDateError(
                f"Historic data only available until 1999-01-04 (tried {parsed_date})."
            )
        if parsed_date > get_current_date():
            raise e.InvalidDateError(f"No future data available (tried {parsed_date}).")
        return parsed_date

    def get_rate(self, currency: str, date: str) -> float:
        """Get EUR exchange rate for a currency"""
        date = self.date_validated(date)
        if self.historic_rates is None:
            self.historic_rates = get_rates_from_dump()
        if date in self.historic_rates and currency in self.historic_rates[date]:
            self.log.info(f"hit: historic rate for {currency} on {date}")
            return self.historic_rates[date][currency]
        self.log.info(f"miss: historic rate for {currency} on {date}")
        api_rates = get_rates_from_api(date=date)
        if currency in api_rates:
            self.log.info(f"hit: api rate for {currency} on {date}")
            return api_rates[currency]
        self.log.info(f"miss: api rate for {currency} on {date}")
        raise e.WrongCurrencyCodeError(
            f"The exchange rate for {currency} ({date}) is not available."
        )

    def exchange(self, value: float, from_currency: str, to_currency: str, date: str) -> float:
        """Convert value from one currency to another"""
        # convert to base currency (EUR) except if coming from EUR already
        value_in_eur = (
            value / self.get_rate(currency=from_currency, date=date)
            if from_currency != "EUR"
            else value
        )
        # convert to target currency except if target currency is EUR
        return (
            value_in_eur * self.get_rate(currency=to_currency, date=date)
            if to_currency != "EUR"
            else value_in_eur
        )

    def yield_default_from_currency(self) -> Generator[str, None, None]:
        """Provide the default FROM currency code"""
        while True:
            yield self.from_currency

    def yield_default_to_currency(self) -> Generator[str, None, None]:
        """Provide the default TO currency code"""
        while True:
            yield self.to_currency

    def yield_default_date(self) -> Generator[str, None, None]:
        """Provide the default date"""
        while True:
            yield self.date

    def transform(self, inputs: Sequence[Sequence[str]]) -> Sequence[str]:
        """Do the actual transformation of values"""
        value_input = inputs[0]
        try:
            from_currency_input = iter(inputs[1])
        except IndexError:
            from_currency_input = self.yield_default_from_currency()
        try:
            to_currency_input = iter(inputs[2])
        except IndexError:
            to_currency_input = self.yield_default_to_currency()
        try:
            date_input = iter(inputs[3])
        except IndexError:
            date_input = self.yield_default_date()

        return [
            str(
                self.exchange(
                    value=float(_),
                    from_currency=next(from_currency_input),
                    to_currency=next(to_currency_input),
                    date=next(date_input),
                )
            )
            for _ in value_input
        ]
