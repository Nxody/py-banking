from decimal import Decimal
from datetime import datetime, timezone

from classes.definitions import Currency

class Account:
    def __init__(
        self,
        account_id: int,
        user_id: int,
        currency: Currency,
        balance: Decimal = Decimal("0.00"),
        created_at: datetime = None,
        is_active: bool = True,
    ):
        self.account_id = account_id
        self.user_id = user_id
        self.currency = currency
        self.balance = balance
        self.created_at = created_at or datetime.now(timezone.utc)
        self.is_active = is_active

    def deposit(self, amount: Decimal):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount

    def withdraw(self, amount: Decimal):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount

    def get_balance(self) -> Decimal:
        return self.balance

    def close(self):
        self.is_active = False

    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "user_id": self.user_id,
            "currency": self.currency.value,
            "balance": str(self.balance),
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active,
        }