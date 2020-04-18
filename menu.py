import tkinter as tk
from labeled_entry import LabeledEntry
from game import Game
from portfolio import Portfolio
import tkinter.messagebox as messagebox

class Menu(tk.Frame):
    def __init__(self, master, categories):
        super().__init__(master)
        self.categories = categories
        self.master = master
        self.create_items()

    def create_items(self):
        self.months = LabeledEntry(self, "months")
        self.tax_rate = LabeledEntry(self, "Tax rate")
        self.initial_cash = LabeledEntry(self, "Initial cash")
        self.months.pack()
        self.tax_rate.pack()
        self.initial_cash.pack()
        self.button = tk.Button(self, text="Start", command=self.apply)
        self.button.pack()
        self.pack()

    def apply(self):
        try:
            months = int(self.months.get_text())
            tax_rate = float(self.tax_rate.get_text()) / 100
            initial_cash = float(self.initial_cash.get_text())
            portfolio = Portfolio(self.categories, tax_rate, months)
            portfolio.add_cash(initial_cash)
            master = self.master
            if tax_rate < 0 or tax_rate > 1:
                raise Exception("Bad tax rate")

            if months < 12 or months > 30:
                raise Exception("Bad months count")

            self.pack_forget()
            self.destroy()
            Game(master=master, portfolio=portfolio).mainloop()
        except Exception as ex:
            messagebox.showerror("Error", message=str(ex))

