import datetime

from classes.Account import Account
from classes.Transaction import Transaction
from classes.User import User
from classes.definitions import Currency, TransactionType

import sqlite3, os
import random


class BankService:
    def __init__(self): #, exchange_service: ExchangeRateService):
        path = "storage.db"
        if os.path.exists(path):
            self.con = sqlite3.connect(path)
            self.cur = self.con.cursor()
        else:
            raise Exception("SQLite file doesn't exist")

    def __validate_meta(self):
        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS "transactions" (
                "transaction_id" INTEGER NULL,
                "from_account_id" INTEGER NULL,
                "to_account_id" INTEGER NULL,
                "transaction type" VARCHAR(50) NULL,
                "amount" INTEGER NULL,
                "currency_id" VARCHAR(50) NULL,
                "created_at" INTEGER NULL,
                "description" VARCHAR(50) NULL,
                "exchange_rate" INTEGER NULL
            );
            
            CREATE TABLE IF NOT EXISTS "users" (
                "user_id" INTEGER NULL,
                "account_id" INTEGER NULL,
                "currency_id" VARCHAR(50) NULL DEFAULT NULL,
                "balance" INTEGER NULL,
                "created_at" DATETIME NULL,
                "is_active" TINYINT NULL
            );
        """)

    # Users
    def create_user(self, username: str, email: str, password_hash: str, first_name: str, last_name: str) -> User:
        while True:
            user_id = str(random.randint(0,9999999))
            while len(user_id) < 7:
                user_id = f"0{user_id}"
            user_id = f"U{user_id}"
            ret = self.cur.execute("SELECT * FROM users WHERE user_id = ?", [user_id]).fetchone()
            if not ret:
                break
        self.cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, username, email, password_hash, first_name, last_name, "EUR", datetime.datetime.now().timestamp(), 1))
        self.con.commit()
        return self.get_user(user_id)

    def get_user(self, user_id: str) -> User:
        ret = self.cur.execute("SELECT * FROM users WHERE user_id = ?", [user_id]).fetchone()
        if ret:
            return User(
                user_id=ret[0],
                username=ret[1],
                email=ret[2],
                password_hash=ret[3],
                first_name=ret[4],
                last_name=ret[5],
                created_at=ret[6],
                is_active=ret[7],
            )
        raise Exception('This user does not exist')

    def deactivate_user(self, user_id: str):
        self.cur.execute("UPDATE users SET is_active = 0 WHERE user_id = ? AND is_active = 1", [user_id])
        self.con.commit()

    # Accounts
    def create_account(self, user_id: str, currency: Currency) -> Account:
        while True:
            acc_id = str(random.randint(0, 9999999))
            while len(acc_id) < 7:
                acc_id = f"0{acc_id}"
            acc_id = f"A{acc_id}"
            ret = self.cur.execute("SELECT * FROM accounts WHERE account_id = ?", [acc_id]).fetchone()
            if not ret:
                break
        self.cur.execute("INSERT INTO accounts VALUES(?, ?, ?, ?, ?, ?)", (user_id, acc_id, currency.value, 0, datetime.datetime.now(), 1))
        self.con.commit()
        return self.get_account(acc_id)

    def get_account(self, account_id: str) -> Account:
        ret = self.cur.execute("SELECT * FROM accounts WHERE account_id = ?", [account_id]).fetchone()
        if ret:
            return Account(
                user_id=ret[0],
                account_id=ret[1],
                currency=Currency[ret[2]],
                balance=ret[3],
                created_at=ret[4],
                is_active=ret[5],
            )
        raise Exception('This account does not exist')

    def get_user_accounts(self, user_id: str) -> list[Account]:
        ret = self.cur.execute("SELECT * FROM accounts WHERE user_id = ?",[user_id]).fetchall()
        list = []
        if ret:
            for i in ret:
                list.append(Account(
                    user_id=i[0],
                    account_id=i[1],
                    currency=Currency[i[2]],
                    balance=i[3],
                    created_at=i[4],
                    is_active=i[5],
                ))
        return list

    def deposit(self, account_id: str, amount: int) -> Transaction:
        bal = self.cur.execute("SELECT balance FROM accounts WHERE account_id = ?", [account_id]).fetchone()[0] or 0
        try:
            bal += int(amount)
            if bal >= 0:
                self.cur.execute("UPDATE accounts SET balance = ? WHERE account_id = ?", [bal, account_id])
                self.con.commit()
                return self._transaction(int(datetime.datetime.now().timestamp()), 'ATM', account_id, TransactionType.DEPOSIT, int(amount), Currency.EUR, datetime.datetime.now(), 'Deposit', 1)
        except Exception():
            y = 0


    def withdraw(self, account_id: str, amount: int) -> Transaction:
        bal = self.cur.execute("SELECT balance FROM accounts WHERE account_id = ?", [account_id]).fetchone()[0] or 0
        try:
            bal -= int(amount)
            if bal >= 0:
                self.cur.execute("UPDATE accounts SET balance = ? WHERE account_id = ?", [bal, account_id])
                self.con.commit()
                return self._transaction(int(datetime.datetime.now().timestamp()), account_id, 'ATM', TransactionType.WITHDRAWAL, int(amount), Currency.EUR, datetime.datetime.now(), 'Withdrawl', 1)
        except Exception():
            y = 0

    def transfer(self, from_account_id: str, to_account_id: str, amount: int) -> Transaction|None:
        bal1 = self.cur.execute("SELECT balance FROM accounts WHERE account_id = ?", [from_account_id]).fetchone()[0] or 0
        bal2 = self.cur.execute("SELECT balance FROM accounts WHERE account_id = ?", [to_account_id]).fetchone()[0] or 0
        try:
            bal1 -= int(amount)
            bal2 += int(amount)
        except Exception():
            y = 0

        if bal1 >= 0:
            self.cur.execute("UPDATE accounts SET balance = ? WHERE account_id = ?", [bal1, from_account_id])
            self.cur.execute("UPDATE accounts SET balance = ? WHERE account_id = ?", [bal2, to_account_id])
            self.con.commit()
            return self._transaction(int(datetime.datetime.now().timestamp()), from_account_id, to_account_id,
                                     TransactionType.TRANSFER, amount, Currency.EUR, datetime.datetime.now(),
                                     'Transfer', 1)
        return False

    def _transaction(self, transaction_id, from_account_id, to_account_id, transaction_type, amount, currency, created_at, description, exchange_rate) -> Transaction:
        self.cur.execute("INSERT INTO transactions VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (transaction_id, from_account_id, to_account_id, transaction_type.value, int(amount), currency.value, created_at, description, exchange_rate))
        self.con.commit()
        return Transaction(transaction_id, from_account_id, to_account_id, transaction_type, amount, currency, created_at, description, exchange_rate)

    def get_transactions(self, account_id):
        ret = self.cur.execute("SELECT from_account_id, to_account_id, amount, description FROM transactions WHERE from_account_id = ? OR to_account_id = ? ORDER BY transaction_id DESC", [account_id, account_id]).fetchall()
        list = []
        for row in ret:
            list.append({'from_account_id': row[0], 'to_account_id': row[1], 'balance':row[2], 'transaction_type':row[3]})
        return list