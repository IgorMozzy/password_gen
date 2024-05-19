import tkinter as tk
from tkinter import ttk

from service import PasswordGenerator, WrongParamsException


class PasswordGeneratorTkinter:
    def __init__(self):
        self.passgen = PasswordGenerator()
        self.entry = None
        self.info = None
        self.root = tk.Tk()
        self.root.title("Password Generator")
        self.root.geometry("340x170")
        self.root.resizable(False, False)

        self.include_letters = tk.BooleanVar(value=True)
        self.include_digits = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)
        self.length = tk.IntVar(value=12)
        self.text = tk.StringVar(value='')
        self.info_text = tk.StringVar(value='')

        self.create_ui()

    def create_ui(self):

        for c in range(6):
            self.root.columnconfigure(index=c, weight=1)
        for r in range(4):
            self.root.rowconfigure(index=r, weight=0)

        # Блок с выбором опций
        rb1_frame = ttk.Frame(self.root, borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        rb1_frame.grid(row=1, column=0, columnspan=4, ipadx=0, ipady=0, padx=10, pady=0)

        rb1_label = ttk.Label(rb1_frame, text="Options")
        rb1_label.pack()

        rb1_1 = ttk.Checkbutton(rb1_frame, text="Letters", variable=self.include_letters)
        rb1_2 = ttk.Checkbutton(rb1_frame, text="Digits", variable=self.include_digits)
        rb1_3 = ttk.Checkbutton(rb1_frame, text="Symbols", variable=self.include_symbols)

        rb1_1.pack(side=tk.LEFT, anchor=tk.W)
        rb1_2.pack(side=tk.LEFT, anchor=tk.W)
        rb1_3.pack(side=tk.LEFT, anchor=tk.W)

        # Блок с длиной пароля и кнопкой генерации
        b1_frame = ttk.Frame(self.root, borderwidth=0, padding=[8, 10])
        b1_frame.grid(row=1, column=4, columnspan=2, ipadx=0, ipady=0, padx=0, pady=0)

        b1_label = ttk.Label(b1_frame, text="Length")
        b1_label.pack()

        e_symb = ttk.Entry(b1_frame, width=10, textvariable=self.length)
        e_symb.pack(padx=0, pady=5)

        b1_button = ttk.Button(b1_frame, text="Generate")
        b1_button.pack()
        b1_button.bind("<ButtonPress>",  self.get_pass)

        # Блок с инфо
        information = ''
        info_frame = ttk.Frame(borderwidth=0, padding=[0, 0])
        self.info = ttk.Label(info_frame, text=information, foreground="#B71C1C")
        self.info.pack()

        info_frame.grid(row=2, column=0, columnspan=6, ipadx=0, ipady=0, padx=0, pady=0)

        # Блок с полем вывода
        entry_frame = ttk.Frame(borderwidth=0, padding=[8, 10])
        self.entry = ttk.Entry(entry_frame, width=300, textvariable=self.text)
        self.entry.pack()

        entry_frame.grid(row=3, column=0, columnspan=6, ipadx=0, ipady=0, padx=0, pady=0)

    def get_pass(self, _):
        # Очистка поля вывода, генерация нового пароля и размещение в поле
        try:
            self.passgen.set_params(self.length.get(), self.include_letters.get(),
                                    self.include_digits.get(), self.include_symbols.get())
            password = self.passgen.generate_password()
            self.info['text'] = ''
            self.entry.delete(0, tk.END)
            self.entry.insert(0, password)
        except (WrongParamsException, TypeError, ValueError) as e:
            self.info['text'] = e

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = PasswordGeneratorTkinter()
    app.start()
