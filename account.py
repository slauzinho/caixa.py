from __future__ import print_function
import os
import pickle


class Account(object):
    """
    This class has the transactions and the current balance of bank account.

    """

    def __init__(self, transactions=None, saldo=0):
        self.saldo = saldo
        """float: Current account balance."""
        if transactions is None:
            self.transactions = []
        else:
            self.transactions = transactions
            """list:  All the transactions."""
        self.new_mov = []

    def __repr__(self):
        return 'Saldo=%s, Movimentos Atuais=%s, Novos Movimentos=%s' % \
                (self.saldo, self.transactions, self.new_mov)

    @classmethod
    def load(cls):
        """
        Load the previously saved Account.

        We use this function to get the previously saved data if it can't find
        the file or if the file is empty it means there is nothing to load.

        Returns:
            An Account containing previously saved data or an empty one.

        """
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

    def update(self, new_account):
        """
        Update our class with new values.

        This function is used to update the values of our currently class using,
        by comparing it another one.
        Copies the saldo from the new account.
        Use the new_transactions function to get the new transactions and add
        it to the end of our transactions list.

        Args:
            new_account (Account): The Account we wanna update from.

        """
        self.saldo = new_account.saldo
        self.new_mov = new_transactions(self.transactions, new_account.transactions)
        self.transactions += self.new_mov

    def save(self):
        """
        Save the Account in a file.

        This function is used to save all the Account data into a file named
        "caixadirecta.dat".

        """
        trans_file = os.path.expanduser('caixadirecta.dat')

        with open(trans_file, 'wb') as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

def new_transactions(transactions_db, transactions):
    """
    Find a list of new transactions.

    Finds the sequence that's present in transactions and in transactions_db

    Args:
        transactions_db (list): All previous transactions saved.
        transactions (list): The ten most recent transactions scraped.

    Returns:
        b (list): The new transactions sequence.

    """
    a_len = len(transactions_db)
    b = transactions[::-1]

    for i in range(a_len):
        if transactions_db[i:] == b[:a_len-i]:
            return b[a_len-i:]
    return b
