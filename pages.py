import os
from decimal import Decimal

from classes.Account import Account
from classes.BankService import BankService
from classes.definitions import Currency
from classes.User import User


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Pages():
    def __init__(self, bs: BankService):
        self.bs = bs
        self.userObj: User|None = None
        self.accObj: list[Account] = []

        self.no_login()

    def pexit(self):
        clear()
        print('Goodbye :)')
        exit()

    def register(self):
        clear()
        print('-' * 150)
        em = input('Enter Email: ')
        ps = input('Enter Password: ')
        fn = input('Enter Firstname: ')
        ln = input('Enter Lastname:  ')
        self.userObj = self.bs.create_user('', em, ps, fn, ln)
        self.accObj = [self.bs.create_account(self.userObj.user_id, Currency.EUR)]
        print('-' * 150)
        self.loggedin()

    def login(self):
        clear()
        print('-' * 150)
        userid = input('Enter UserId: ')
        pswd = input('Enter Password: ')
        print('-' * 150)
        temp_user_obj = self.bs.get_user(user_id=userid)
        if not temp_user_obj:
            input('Login failed. Press any key to continue...')
            self.no_login()
        else:
            if not temp_user_obj.password_hash == pswd:
                input('Login failed. Press any key to continue...')
                self.no_login()
            else:
                self.userObj = temp_user_obj
                self.accObj = self.bs.get_user_accounts(self.userObj.user_id)
                self.loggedin()

    def loggedin(self):
        clear()
        self.accObj = self.bs.get_user_accounts(self.userObj.user_id)
        bal = 0
        curr = self.accObj[0].currency
        for acc in self.accObj:
            if acc.currency == curr:
                bal += acc.balance
        print(f"""
{'-'*150}
Welcome {self.userObj.first_name} {self.userObj.last_name} [{self.userObj.user_id}]
Your balance is {curr.value} {bal}
{'-'*150}
Actions:
  [1] Deposit
  [2] Withdraw
  [3] Send
  [4] View transactions
  [5] Exit
{'-'*150}
        """)
        action = str(input('What do you want to do: '))
        if action == '1':
            self.deposit()
        elif action == '2':
            self.withdraw()
        elif action == '3':
            self.send()
        elif action == '4':
            self.transactions()
        else:
            self.pexit()

    def deposit(self):
        print('-'*150)
        amount = input('Enter amount: ')
        try:
            amount = int(amount)
        except Exception as e:
            input('Unable to add balance. Press any key to continue...')
        self.bs.deposit(self.accObj[0].account_id, amount)
        input('Balance added. Press any key to continue...')
        self.loggedin()

    def withdraw(self):
        print('-'*150)
        amount = input('Enter amount: ')
        try:
            amount = int(amount)
        except Exception:
            input('Unable to remove balance. Press any key to continue...')
        self.bs.withdraw(self.accObj[0].account_id, amount)
        input('Balance removed. Press any key to continue...')
        self.loggedin()

    def send(self):
        print('-'*150)
        acc = input('Enter target account: ')
        amount = input('Enter amount: ')
        try:
            self.bs.transfer(self.accObj[0].account_id, acc, Decimal(amount))
            input('Balance transfered. Press any key to continue...')
        except Exception:
            input('Unable to transfer balance. Press any key to continue...')
        self.loggedin()

    def transactions(self):
        clear()
        print('-'*150)
        print(f'Transactions for {self.accObj[0].account_id}')
        print('-' * 150)
        for row in self.bs.get_transactions(self.accObj[0].account_id):
            print(f'{row['from_account_id']} | {row['to_account_id']} | {row['balance']} | {row['transaction_type']}')
        print('-' * 150)
        input('Press any key to return...')
        self.loggedin()

    def no_login(self):
        clear()
        print(f"""
{'-'*150}
Choose action:
[1] Login
[2] Register
[3] Exit
{'-'*150}
        """)
        action = input()
        print('-'*150)
        if action == "1":
            self.login()
        elif action == "2":
            self.register()
        else:
            self.pexit()
