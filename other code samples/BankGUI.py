""""BangGUI. py -- Hana Galijasevic - hg343 - OOP SP2021 - Prof. Tim Barron"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import logging

from sqlalchemy import create_engine
from Bank import Base
from sqlalchemy.orm.session import sessionmaker

from Bank import Bank, Transaction, Account

logging.basicConfig(filename='bank.log', level=logging.DEBUG, datefmt='%Y-%m-%d %I:%M:%S',
                    format='%(asctime)s|%(levelname)s|%(message)s')



class Menu:
    """Display a menu and respond to choices when run."""


    def __init__(self, session):
        self._window = tk.Tk()
        self._window.report_callback_exception = handle_exception

        self._window.title(f"BANK")
        self._session = session
        self.acc_selected = None
        try:
            self._bank = self._session.query(Bank).first()
            logging.debug('Loaded from bank.db')
        except:
            pass

        self._options_frame = tk.Frame(self._window)
        self._list_frame = tk.Frame(self._window)
        self._account_frame = tk.Frame(self._window)
        self._transactions_frame = tk.Frame(self._window)
        self._selected_acc = tk.Frame(self._window)
        self._selected_acc.grid(row=1, column=1, columnspan=3)


        self.accos = tk.StringVar()
        if self.accos is not None:
            self.l = tk.Label(self._selected_acc, text=f"Selected account: {self.accos.get()}")
        else:
            self.l = tk.Label(self._selected_acc, text=f"Selected account: ")

        self.l.grid(row=1, column=1)

        tk.Button(self._options_frame, text="Open Account", command=self._open_account).grid(row=1, column=1, columnspan=2),
        tk.Button(self._options_frame, text="Add Transaction", command=self._add_transaction).grid(row=1, column=6),
        tk.Button(self._options_frame, text="Monthly Triggers", command=self._mt).grid(row=1, column=7),


        self._options_frame.grid(row=2, column=1, columnspan=6)
        self._list_frame.grid(row=3, column=1, columnspan=2, sticky="w")
        self._account_frame.grid(row=4, column=1, columnspan=2, rowspan=5)
        self._transactions_frame.grid(row=3, column=3, columnspan=3, sticky="ne")
        self.text = tk.Text(self._transactions_frame, width=30)

        l1 = tk.Label(self._account_frame, text="Accounts:")
        self._accounts = {}
        self._summary()
        logging.debug('Saved to bank.db')
        self._window.mainloop()


    def _summary(self):
        # t = ""
        self.row = 8
        self._list_frame.destroy()
        self._list_frame = tk.Frame(self._window)
        self._list_frame.grid(row=3, column=1, columnspan=2, sticky="w")
        if self.acc_selected is not None:
            self._list_transactions(self.acc_selected)
            self.l.destroy()
            tmpb = "${:,.2f}".format(self.acc_selected.balance)
            self.l = tk.Label(self._selected_acc, text=f"Selected account: {self.acc_selected.name},\tbalance: {tmpb}")
            self.l.grid(row=1, column=1)

        for banks in self._session.query(Bank):
            self._accounts[banks.accounts[0].number] = banks.accounts[0]
            tmp = banks.summary()
            temp = ttk.Radiobutton(self._list_frame, text=tmp[0], variable=self.accos, value=tmp[0],
                                   command=self._select_account)

            temp.grid(row=self.row, column=0, sticky="w")


            self.row+=1

    def _open_account(self, *args):
            session = self._session
            self._summary()
            bank = Bank()
            accType = tk.StringVar()
            c = self._options_frame
            g1 = ttk.Radiobutton(c, text='Savings', variable=accType, value='Savings')
            g2 = ttk.Radiobutton(c, text='Checking', variable=accType, value='Checking')

            def open():
                bank.openAccount(accType.get(), e2.get(), session)
                self._summary()
                e2.destroy()
                b.destroy()
                l1.destroy()
                l2.destroy()
                g1.destroy()
                g2.destroy()

            l1 = tk.Label(self._options_frame, text="Account type:")
            l1.grid(row=1, column=1)
            g1.grid(row=2, column=1)
            g2.grid(row=3, column=1)

            l2 = tk.Label(self._options_frame, text="Initial Deposit: ")
            l2.grid(row=4, column=1)
            e2 = tk.Entry(self._options_frame, text="Initial deposit: ")
            e2.grid(row=5, column=1)
            #
            b = tk.Button(self._options_frame, text="Open Account!", command=open)
            b.grid(row=6, column=1)


    def _select_account(self):
        self.l.destroy()
        self.l = tk.Label(self._selected_acc, text=f"Selected account: {self.accos.get()}")
        self.l.grid(row=1, column=1)
        self.acc_selected = self.AllMatchAccount(self.accos.get())

        if self.accos is not None:
            self._list_transactions(self.acc_selected)

    def _list_transactions(self, name):

        a = name
        t = ""
        i = 1
        i_s = "{:,.1f}".format(i)
        self.text.delete('1.0', tk.END)
        for transactions in a.transactions:
            temp = f'{transactions.date_object},\t{"${:,.2f}".format(transactions.amount)}\n'

            if temp[13] == '-':
                self.text.insert(tk.END, temp)
                self.text.tag_add(temp, i_s, tk.END)
                self.text.tag_config(temp, foreground='red')
            else:
                self.text.insert(tk.END, temp)
                if self.text.tag_ranges(temp):
                    self.text.tag_add(f"{temp}{i}", i_s, tk.END)
                    self.text.tag_config(f"{temp}{i}", foreground='green')
                else:
                    self.text.tag_add(temp, i_s, tk.END)
                    self.text.tag_config(temp, foreground='green')

            i+=1
            i_s = "{:,.1f}".format(i)


        self.text.grid(row=1, column=1)

    def AllMatchAccount(self, name):
        for banks in self._session.query(Bank):
            res = banks.matchAccount(self.accos.get())
            if res is not None:
                return res

        if res is None:
            return None

    def _add_transaction(self):
        session = self._session
        self._summary()
        bank = Bank()
        c = self._options_frame
        g1 = tk.Entry(c, text="Date: ")
        g2 = tk.Entry(c, text="Amount: ")
        tmpa = self.acc_selected
        def addTransaction():
            transaction = Transaction(amount=g2.get(), d=g1.get())
            # bank.openAccount(accType.get(), e2.get(), session)
            transaction.addTransaction(self.acc_selected, transaction, session=session)
            self._summary()
            self.acc_selected = tmpa
            self._list_transactions(self.acc_selected)
            b.destroy()
            l1.destroy()
            l2.destroy()
            g1.destroy()
            g2.destroy()

        l1 = tk.Label(self._options_frame, text="Date:")
        l1.grid(row=2, column=5, sticky="e")
        g1.grid(row=2, column=6, sticky="e")

        l2 = tk.Label(self._options_frame, text="Amount: ")
        l2.grid(row=3, column=5, sticky="e")
        g2.grid(row=3, column=6, sticky="e")
        #
        b = tk.Button(self._options_frame, text="Enter", command=addTransaction)
        b.grid(row=4, column=6)
        # self._summary()



    def _mt(self):
        for bank in self._session.query(Bank):
            bank = bank.mt(self._session)
        logging.debug('Triggered fees and interest')
        self._summary()
        self._list_transactions(self.acc_selected)

def handle_exception(exception, value, traceback):
    if exception.__name__ == "dError":
        msg = "Please try again with a valid date in the format YYYY-MM-DD."
        messagebox.showerror(title="Date Error", message=msg)
        # print()
    elif exception.__name__ == "aError":
        msg = "Please try again with a valid dollar amount."
        messagebox.showerror(title="Amount Error", message=msg)
    elif exception.__name__ == "OverdrawError":
        msg = "This transaction could not be completed due to an "
        "insufficient account balance."
        messagebox.showerror(title="Overdraw Error", message=msg)
    elif exception.__name__ == "TransactionLimitError":
        msg = "This transaction could not be completed because the account has reached a transaction limit."
        messagebox.showerror(title="Limit Error", message=msg)
    elif exception.__name__ == "TransactionOrderError":
        msg = f"New transactions must be from {value.ld} onward."
        messagebox.showerror(title="Date Order Error", message=msg)
    # elif exception.__name__ == "aError":
    else:
        msg = "Sorry! Something unexpected happened. If this problem persists please contact our support team for assistance."

    logging.debug('Saved to bank.db')
    logging.error(f"{exception.__name__}: {repr(value)}")
    sys.exit(1)



if __name__ == "__main__":
    logging.basicConfig(filename='bank.log', level=logging.DEBUG, datefmt='%Y-%m-%d %I:%M:%S',
                        format='%(asctime)s|%(levelname)s|%(message)s')

    engine = create_engine(f"sqlite:///bank.db")
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    Menu(session)