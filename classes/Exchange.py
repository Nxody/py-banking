from decimal import Decimal
from datetime import datetime, timezone

from classes.definitions import Currency

class ExchangeRateService:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self._cache: dict[tuple, tuple[Decimal, datetime]] = {}
        self._cache_ttl_seconds: int = 300

    def get_rate(self, from_currency: Currency, to_currency: Currency) -> Decimal:
        print('API not yet implemented')

    def convert(self, amount: Decimal, from_currency: Currency, to_currency: Currency) -> Decimal:
        rate = self.get_rate(from_currency, to_currency)
        return (amount * rate).quantize(Decimal("0.01"))

    def _is_cache_valid(self, key: tuple) -> bool:
        if key not in self._cache:
            return False
        _, cached_at = self._cache[key]
        return (datetime.now(timezone.utc) - cached_at).seconds < self._cache_ttl_seconds

    def _store_in_cache(self, key: tuple, rate: Decimal):
        self._cache[key] = (rate, datetime.now(timezone.utc))