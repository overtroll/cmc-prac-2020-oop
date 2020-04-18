import tkinter as tk
import tkinter.messagebox as messagebox
from inspect import getfullargspec
from portfolio import Portfolio
from labeled_entry import LabeledEntry
import sys


class ActionFrame(tk.Frame):
    def __init__(self, master, function, portfolio):
        super().__init__(master)
        self.master = master
        self.function = function
        self.portfolio = portfolio
        self.create_items()

    def create_items(self):
        params = getfullargspec(self.function).args[1:]
        self.entries = []
        for param in params:
            entry = LabeledEntry(self, param)
            entry.pack()
            self.entries.append(entry)

        name = self.function.__name__
        self.button = tk.Button(self, text=name, command=self.apply)
        self.button.pack()

    def apply(self):
        args = [entry.get_text() for entry in self.entries]
        try:
            self.function(self.portfolio, *args)
            self.master.draw()
        except Exception as ex:
                messagebox.showerror("Error", message=str(ex))


class Game(tk.Frame):
    def __init__(self, portfolio, master=None):
        super().__init__(master)
        self.portfolio = portfolio
        self.master = master
        self.pack()
        self.create_items()
        self.draw()

    def create_items(self):
        self.stats = tk.Label(self)
        self.stats.pack(side=tk.LEFT)
        self.buttons = {}


        self.categories = []
        for category in self.portfolio.categories():
            label = tk.Label(self)
            label.pack()
            self.categories.append((label, category))

        self.header = tk.Label(self)
        self.header.pack()

        def next_month(portfolio):
            portfolio.month(
                on_info=lambda message: messagebox.showinfo(message=message))

        for function in [Portfolio.buy,
                         Portfolio.sell,
                         next_month]:
            action_frame = ActionFrame(self, function, portfolio=self.portfolio)
            self.buttons[function.__name__] = action_frame
            action_frame.pack()

        self.exit = tk.Button(self, text="Exit", command=lambda: sys.exit(0))
        self.exit.pack()

    def draw(self):
        self.stats['text'] = self.portfolio.stats()
        self.header['text'] = self.portfolio.header()
        for label, category in self.categories:
            label['text'] = str(category)

        if self.portfolio.game_over():
            button = self.buttons["next_month"]
            button.button["state"] = tk.DISABLED
            messagebox.showinfo("Game over", "Game over")
