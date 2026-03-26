from classes.BankService import BankService

def prepare_service():
    try:
        bank_service = BankService({ "host": "localhost", "port": 3306, "database": "banking", "user": "root", "password": "" })
        print('Connected to database')
        return bank_service
    except Exception as e:
        raise Exception(f'Error connecting to database: {e}')


if __name__ == "__main__":
    bank_service = prepare_service()