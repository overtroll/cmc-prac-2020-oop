import portfolio
import sys

from category import Category
from stock import Stock
from bond import Bond
from bank_deposit import BankDeposit
from portfolio import Portfolio
from metal import Metal
from app import App
from tkinter import Tk


def main():
    categories = [
        Category("Stocks", Stock.factory()),
        Category("Bank deposits", BankDeposit.factory()),
        Category("Precious metals", Metal.factory()),
        Category("Bonds", Bond.factory())
    ]

    portfolio = Portfolio(categories)
    root = Tk()
    app = App(master=root, portfolio=portfolio)
    app.mainloop()


if __name__ == "__main__":
    main()
