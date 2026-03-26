from classes.Account import Account
from classes.Exchange import ExchangeRateService
from classes.Transaction import Transaction
from classes.User import User
from classes.definitions import Currency, TransactionType

from mysql.connector import pooling
from decimal import Decimal

class BankService:
    def __init__(self, db_config: dict): #, exchange_service: ExchangeRateService): # TBA
        self.pool = pooling.MySQLConnectionPool(
            pool_name="banking_pool",
            pool_size=5,
            **db_config
        )
        #self.exchange_service = exchange_service

    def _get_conn(self):
        return self.pool.get_connection()

    def create_user(self, username: str, email: str, password_hash: str, first_name: str, last_name: str) -> User:
        print('Database not yet implemented')

    def get_user(self, user_id: int) -> User:
        print('Database not yet implemented')

    def update_user(self, user_id: int, **fields) -> User:
        print('Database not yet implemented')

    def deactivate_user(self, user_id: int):
        print('Database not yet implemented')

    def create_account(self, user_id: int, currency: Currency) -> Account:
        print('Database not yet implemented')

    def get_account(self, account_id: int) -> Account:
        print('Database not yet implemented')

    def get_user_accounts(self, user_id: int) -> list[Account]:
        print('Database not yet implemented')

    def deposit(self, account_id: int, amount: Decimal) -> Transaction:
        print('Database not yet implemented')

    def withdraw(self, account_id: int, amount: Decimal) -> Transaction:
        print('Database not yet implemented')

    def transfer(self, from_account_id: int, to_account_id: int, amount: Decimal) -> Transaction:
        print('Database not yet implemented')

    def convert_and_transfer(self, from_account_id: int, to_account_id: int, amount: Decimal) -> Transaction:
        print('Database not yet implemented')

    def get_transaction_history(self, account_id: int, limit: int = 50, offset: int = 0) -> list[Transaction]:
        print('Database not yet implemented')