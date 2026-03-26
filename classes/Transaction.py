from decimal import Decimal
from datetime import datetime, timezone

from classes.definitions import Currency, TransactionType

class Transaction:
    def __init__(
        self,
        transaction_id: int,
        from_account_id: int | None,
        to_account_id: int | None,
        transaction_type: TransactionType,
        amount: Decimal,
        currency: Currency,
        created_at: datetime = None,
        description: str = "",
        exchange_rate: Decimal = None,
    ):
        self.transaction_id = transaction_id
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.currency = currency
        self.created_at = created_at or datetime.now(timezone.utc)
        self.description = description
        self.exchange_rate = exchange_rate

    def to_dict(self) -> dict:
        return {
            "transaction_id": self.transaction_id,
            "from_account_id": self.from_account_id,
            "to_account_id": self.to_account_id,
            "type": self.transaction_type.value,
            "amount": str(self.amount),
            "currency": self.currency.value,
            "created_at": self.created_at.isoformat(),
            "description": self.description,
            "exchange_rate": str(self.exchange_rate) if self.exchange_rate else None,
        }