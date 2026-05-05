from classes.BankService import BankService
from pages import Pages

def prepare_service():
    try:
        bank_service = BankService()
        print('Connected to database')
        return bank_service
    except Exception as e:
        raise Exception(f'Error connecting to database: {e}')

if __name__ == "__main__":
    bsObj = prepare_service()
    pagesObj = Pages(bsObj)
