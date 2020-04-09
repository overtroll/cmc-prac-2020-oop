import tkinter as tk
import tkinter.messagebox as messagebox
from inspect import getfullargspec
from portfolio import Portfolio


class LabeledEntry(tk.Frame):
    def __init__(self, master, label):
        super().__init__(master)
        self.entry = tk.Entry(self)
        self.label = tk.Label(self, text=label)
        self.entry.pack(side=tk.RIGHT)
        self.label.pack(side=tk.LEFT)

    def get_text(self):
        return self.entry.get()


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
        apply = tk.Button(self, text=name, command=self.apply)
        apply.pack()

    def apply(self):
        args = [entry.get_text() for entry in self.entries]
        try:
            self.function(self.portfolio, *args)
            self.master.draw()
        except Exception as ex:
            messagebox.showerror("Error", message=str(ex))


class App(tk.Frame):
    def __init__(self, portfolio, master=None):
        super().__init__(master)
        self.portfolio = portfolio
        self.master = master
        self.pack()
        self.create_items()
        self.draw()

    def create_items(self):
        self.header = tk.Label(self)
        self.header.pack()

        self.categories = []
        for category in self.portfolio.categories():
            label = tk.Label(self)
            label.pack()
            self.categories.append((label, category))

        def next_month(portfolio):
            portfolio.month(
                on_info=lambda message: messagebox.showinfo(message=message))

        for function in [Portfolio.add_cash,
                         Portfolio.remove_cash,
                         Portfolio.buy,
                         Portfolio.sell,
                         next_month]:
            action_frame = ActionFrame(self, function, portfolio=self.portfolio)
            action_frame.pack()

    def draw(self):
        self.header['text'] = self.portfolio.header()
        for label, category in self.categories:
            label['text'] = str(category)
