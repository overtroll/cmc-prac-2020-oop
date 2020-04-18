from tkinter import Tk

from bank_deposit import BankDeposit
from bond import Bond
from category import Category
from menu import Menu
from metal import Metal
from stock import Stock


def main():
    categories = [
        Category("Stocks", Stock.factory()),
        Category("Bank deposits", BankDeposit.factory()),
        Category("Precious metals", Metal.factory()),
        Category("Bonds", Bond.factory())
    ]

    root = Tk()
    menu = Menu(root, categories)
    menu.mainloop()


if __name__ == "__main__":
    main()
