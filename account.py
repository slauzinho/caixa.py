from __future__ import print_function
import os
import pickle


class Account(object):

    def __init__(self, transactions=None, saldo=0):
        self.saldo = saldo
        if transactions is None:
            self.transactions = []
        else:
            self.transactions = transactions
        self.new_mov = []

    def __repr__(self):
        return 'Saldo=%s, Movimentos Atuais=%s, Novos Movimentos=%s' % \
                (self.saldo, self.transactions, self.new_mov)

    # Loads the object from the file "caixadirecta.dat" and returns it
    @classmethod
    def load(cls):
        trans_file = os.path.expanduser('caixadirecta.dat')

        if os.path.exists(trans_file):
            with open(trans_file, 'rb') as f:
                try:
                    account = pickle.load(f)
                except EOFError:
                    return Account()
                else:
                    return Account(transactions=account.transactions, saldo=account.saldo)

        return Account()

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


# Compares two lists items and returns the that exist on the transactions list
# and dont exist already on our DB.
def new_transactions(transactions_db, transactions):
    a_len = len(transactions_db)
    b = transactions[::-1]

    for i in range(a_len):
        if transactions_db[i:] == b[:a_len-i]:
            return b[a_len-i:]
    return b
