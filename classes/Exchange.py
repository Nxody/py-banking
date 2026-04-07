from classes.definitions import Currency

import requests
from decimal import Decimal
from requests.exceptions import RequestException
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://api.frankfurter.dev/v2"


class ExchangeRateService:
    def __init__(self, cache_ttl_seconds: int = 300):
        self._cache: dict[tuple, tuple[Decimal, datetime]] = {}
        self._cache_ttl_seconds = cache_ttl_seconds

    def get_rate(self, from_currency: Currency, to_currency: Currency) -> Decimal:
        if from_currency == to_currency:
            return Decimal("1.0")

        cache_key = (from_currency, to_currency)

        if self._is_cache_valid(cache_key):
            rate, _ = self._cache[cache_key]
            logger.debug(f"Cache hit: {from_currency.value} -> {to_currency.value} = {rate}")
            return rate

        rate = self._fetch_rate(from_currency, to_currency)
        self._cache[cache_key] = (rate, datetime.now(timezone.utc))
        return rate

    def convert(self, amount: Decimal, from_currency: Currency, to_currency: Currency) -> Decimal:
        if amount <= 0:
            raise ValueError("Conversion amount must be positive.")
        rate = self.get_rate(from_currency, to_currency)
        return (amount * rate).quantize(Decimal("0.01"))

    def get_all_rates(self, base_currency: Currency) -> dict[str, Decimal]:
        try:
            response = requests.get(
                f"{BASE_URL}/rates",
                params={"base": base_currency.value},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            return {item["quote"]: Decimal(str(item["rate"])) for item in data}
            return {k: Decimal(str(v)) for k, v in data["rates"].items()}
        except RequestException as e:
            logger.error(f"get_all_rates({base_currency.value}) failed: {e}")
            raise

    def _fetch_rate(self, from_currency: Currency, to_currency: Currency) -> Decimal:
        try:
            response = requests.get(
                f"{BASE_URL}/rates",
                params={
                    "base": from_currency.value,
                    "quotes": to_currency.value,
                },
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            for item in data:
                if item["quote"] == to_currency.value:
                    rate = Decimal(str(item["rate"]))
                    logger.debug(f"Fetched rate {from_currency.value} -> {to_currency.value} = {rate}")
                    return rate
        except RequestException as e:
            logger.error(f"_fetch_rate({from_currency.value} -> {to_currency.value}) failed: {e}")
            raise
        except KeyError:
            raise ValueError(f"Rate for {to_currency.value} not found in response.")

    def _is_cache_valid(self, key: tuple) -> bool:
        if key not in self._cache:
            return False
        _, cached_at = self._cache[key]
        return (datetime.now(timezone.utc) - cached_at).seconds < self._cache_ttl_seconds