### BankCLI Homework - OOP SP2021
# Hana Galijasevic - hg343

"""
BankCLI1.py
    Driver for the CLI
    This may also be a class and may be included in your UML diagram Classes

Bank    -   Top-level container/management class
Account -   Base class for bank accounts maintains a list of transactions in the account
            methods support default behavior, but may be overridden by these next two classes...
CheckingAccount -   accounts with less interest and fewer transaction limits
SavingsAccount  -   accounts with more interest and more transactions limits
Transaction     -   date and amount of deposits/withdrawals

 """

# TODO: Exceptions (6/6)
# TODO: Logging (3/3)
# TODO: SQLite & SQLAlchemy (3/3)
# TODO: GUI (6/6)

"""Exceptions:
1. Listing or adding transactions when no account is selected xxxx <----- check if this is the only left exception when
    dealing with bankCLI and add/list transactions;;; issa lil clunky rn with the if...elses
2. overdrawing an account  xxxx
3. exceeding transaction limits xxxx (??? what do with checking account?)
4. transaction dates given in improper format  xxxx
5. invalid amounts given xxxx
6. adding a transaction out of order xxx
"""

"""Logging:
1. "something unexpected happened" :exc
2. logging.debug messages
3. debug it all
"""

"""SQLite & SQLAlchemy:
1. make classes models for database tables
2. create sqlite database in main
3. create and manage a session from BankCLI.py
"""

"""GUI:
1. preserve all functionality
2. list of accounts and balances always up to date
3. select accounts from this display (widgets)
4. w/ selected account always show all transactions distinctively
5. Handle exceptions in GUI manner
6. still logging other general uncaught exceptions
"""

import sys
import logging
from error_handling import OverdrawError, TransactionLimitError, \
    dError, aError, TransactionOrderError
from sqlalchemy import create_engine
from Bank import Base
from sqlalchemy.orm.session import sessionmaker
import pickle

from Bank import Bank, Transaction, Account

logging.basicConfig(filename='bank.log', level=logging.DEBUG, datefmt='%Y-%m-%d %I:%M:%S',
                    format='%(asctime)s|%(levelname)s|%(message)s')


class Menu:
    def __init__(self, session):
        self.name = "menu"
        self._session = session
        try:
            self._bank = self._session.query(Bank).first()
            logging.debug('Loaded from bank.db')
        except:
            pass

    def run(self):
        """Runs the CLI for Bank, endless while loop until 'quit' command"""
        acc_no = None
        try:
            bank = self._bank
        except Exception:
            bank = None
        acc = None
        while True:
            if (acc is None):
                a = None
            else:
                a = acc.name + ",\tbalance: " + "${:,.2f}".format(acc.balance)

            prompt = f"""Currently selected account: {a}
Enter command\nopen account, summary, select account, \
list transactions, add transaction, <monthly triggers>, save, load, quit\n>"""

            try:
                command = input(prompt)

                if command != "quit":
                    if command == "open account":
                        type_of_account = input("Type of account? (checking/savings)\n>")
                        inDeposit = float(input("Initial deposit amount?\n>"))

                        bank = Bank()
                        bank = bank.openAccount(accType=type_of_account, initDep=inDeposit, session=self._session)

                        self._session.commit()
                        if bank:
                            for banks in self._session.query(Bank):
                                banks.summary()


                    if command == "select account":
                        if bank:
                            for banks in self._session.query(Bank):
                                banks.summary()
                            acc_no = int(input("Enter account number\n>"))
                            for banks in self._session.query(Account):
                                if banks.number == acc_no:
                                    acct = banks
                            acc = acct
                        else:
                            raise

                    if command == "summary":
                        if bank:
                            for banks in self._session.query(Bank):
                                banks.summary()
                        else:
                            raise

                    try:
                        if command == "add transaction":

                            if acc_no is not None:  # don't want to have to input all date and amt if no account selected
                                d = input("Date? (YYYY-MM-DD)\n>")
                                amt = input("Amount?\n>")
                                t = Transaction(amt, d)
                                t.addTransaction(acc, t, session=self._session)
                                self._session.commit()
                            else:
                                raise AttributeError

                        if command == "list transactions":
                            if acc_no is not None:
                                # tmpacc = self._session.query(Account).where(Account.number == acc_no).first()
                                acc.listTransactions()
                            else:
                                raise AttributeError

                    except dError:
                        print("Please try again with a "
                              "valid date in the format YYYY-MM-DD.")
                    except aError:
                        print("Please try again with a "
                              "valid dollar amount.")
                    except OverdrawError:
                        print("This transaction could not be completed due to an "
                              "insufficient account balance.")
                    except TransactionLimitError:
                        print("This transaction could not be completed because "
                              "the account has reached a transaction limit.")
                    except TransactionOrderError as e:
                        print(f"New transactions must be from {e.ld} onward.")
                    except AttributeError:
                        print("That command requires that you first select an account.")

                    except Exception as e:
                        print("Unexpected error: ", e)

                    if command == "<monthly triggers>":
                        if bank:
                            bank = bank.mt(self._session)
                            logging.debug('Triggered fees and interest')
                        else:
                            raise

                    if command == "save":
                        pickle.dump(bank, open("bank.pickle", "wb"))
                        logging.debug('Saved to bank.pickle')
                        self._session.commit()
                        logging.debug('Saved to bank.db')


                    if command == "load":
                        bank = pickle.load(open("bank.pickle", "rb"))
                        logging.debug('Loaded from bank.pickle')
                else:
                    logging.debug('Saved to bank.db')
                    break


            except Exception as e:
                e_type = type(e).__name__
                e_message = repr(str(e))
                # print(e)
                print("Sorry! Something unexpected happened. "
                      "If this problem persists please contact our support team for assistance.")
                logging.debug(f'{e_type}: {e_message}')
                sys.exit(0)


if __name__ == "__main__":
    logging.basicConfig(filename='bank.log', level=logging.DEBUG, datefmt='%Y-%m-%d %I:%M:%S',
                        format='%(asctime)s|%(levelname)s|%(message)s')

    engine = create_engine(f"sqlite:///bank.db")
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    menu = Menu(session)
    menu.run()
