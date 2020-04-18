import tkinter as tk


class LabeledEntry(tk.Frame):
    def __init__(self, master, label):
        super().__init__(master)
        self.entry = tk.Entry(self)
        self.label = tk.Label(self, text=label)
        self.entry.pack(side=tk.RIGHT)
        self.label.pack(side=tk.LEFT)

    def get_text(self):
        return self.entry.get()
