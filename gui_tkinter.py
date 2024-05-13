import tkinter as tk
from tkinter import ttk

from main import generate_password

root = tk.Tk()
root.title("Password Generator")
root.geometry("340x150")
root.resizable(False, False)

for c in range(6): root.columnconfigure(index=c, weight=1)
for r in range(4): root.rowconfigure(index=r, weight=0)


include_letters = tk.BooleanVar(value=True)
include_digits = tk.BooleanVar(value=True)
include_symbols = tk.BooleanVar(value=True)

rb1_frame = ttk.Frame(borderwidth=1, relief=tk.SOLID, padding=[8, 10])
rb1_label = ttk.Label(rb1_frame, text="Options")
rb1_label.pack()

rb1_1 = ttk.Checkbutton(rb1_frame, text="Letters", variable=include_letters)
rb1_2 = ttk.Checkbutton(rb1_frame, text="Digits", variable=include_digits)
rb1_3 = ttk.Checkbutton(rb1_frame, text="Symbols", variable=include_symbols)
rb1_1.pack(side=tk.LEFT, anchor=tk.W)
rb1_2.pack(side=tk.LEFT, anchor=tk.W)
rb1_3.pack(side=tk.LEFT, anchor=tk.W)

rb1_frame.grid(row=1, column=0, columnspan=4, ipadx=0, ipady=0, padx=10, pady=0)

length = tk.IntVar(value=12)

text = tk.StringVar(value='')

result = ''

entry_frame = ttk.Frame(borderwidth=0, padding=[8, 10])
entry = ttk.Entry(entry_frame, width=300, textvariable=text)
entry.pack()
entry_frame.grid(row=2, column=0, columnspan=6, ipadx=0, ipady=0, padx=0, pady=0)


def passgen(_):
    entry.delete(0, tk.END)
    entry.insert(0, generate_password(length.get(), include_letters.get(), include_digits.get(), include_symbols.get()))


b1_frame = ttk.Frame(borderwidth=0, padding=[8, 10])
b1_label = ttk.Label(b1_frame, text="Length")
e_symb = ttk.Entry(b1_frame, width=10, textvariable=length)
b1_button = ttk.Button(b1_frame, text="Generate")
b1_button.bind("<ButtonPress>", passgen)
b1_label.pack()
e_symb.pack(padx=0, pady=5)
b1_button.pack()
b1_frame.grid(row=1, column=4, columnspan=2, ipadx=0, ipady=0, padx=0, pady=0)

root.mainloop()
