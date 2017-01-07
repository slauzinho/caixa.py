import os
import pickle

class Account():

    def __init__(self, transactions, saldo):
        self.saldo = saldo
        self.transactions = transactions
        self.new_mov = []

    # Updates the class with the new transactions and the new account balance
    def update(self, new_account):
        self.saldo = new_account.saldo
        self.new_mov = new_transactions(self.transactions, new_account.transactions)
        self.transactions += self.new_mov

    # Saves the object for later
    def save(self):
        trans_file = os.path.expanduser('caixadirecta.dat')

        with open(trans_file, 'wb') as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)
            f.close()

    # Loads the object from the file "caixadirecta.dat" and returns it
    @staticmethod
    def load():
        trans_file = os.path.expanduser('caixadirecta.dat')
        account = Account([],0)

        if os.path.exists(trans_file):
            with open(trans_file, 'rb') as f:
                account = pickle.load(f)
                f.close()

        return account

# Compares two lists items and returns the that exist on the transactions list
# and dont exist already on our DB.
def new_transactions(transactions_db, transactions):
    temp = []
    if len(transactions_db) == len(transactions):
        return temp

    if len(transactions_db) < len(transactions):
        temp = transactions[len(transactions_db):]

    else:
        s = set(transactions_db)
        temp = [x for x in transactions if x not in s]

    return temp
