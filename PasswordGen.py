import random
import tkinter as tk
from tkinter import messagebox


def generate_password(length, letters, numbers):
    if letters and numbers:
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    elif letters:
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    elif numbers:
        chars = '0123456789'
    else:
        messagebox.showerror('Error', 'No options selected for password generation.')
        return

    password = ''
    for i in range(length):
        password += random.choice(chars)

    return password


def copy_to_clipboard(password):
    app.clipboard_clear()
    app.clipboard_append(password)


def show_password(password):
    password_window = tk.Toplevel(app)
    password_window.title('Generated Password')
    
    tk.Label(password_window, text='Your password is:').grid(row=0, column=0)
    tk.Label(password_window, text=password, font=("Helvetica", 14)).grid(row=1, column=0)
    tk.Button(password_window, text='Copy to Clipboard', command=lambda: copy_to_clipboard(password)).grid(row=2, column=0)
    tk.Button(password_window, text='Close', command=password_window.destroy).grid(row=3, column=0)


def on_submit():
    try:
        length = int(length_entry.get())
        if length < 3 or length > 20:
            raise ValueError()
    except ValueError:
        messagebox.showerror('Error', 'Invalid password length. Enter a number between 3 and 20.')
        return

    letters = letters_var.get()
    numbers = numbers_var.get()

    password = generate_password(length, letters, numbers)

    if password:
        show_password(password)


app = tk.Tk()
app.title('Password Generator')

letters_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)

tk.Label(app, text='Include letters?').grid(row=0, column=0)
tk.Checkbutton(app, variable=letters_var).grid(row=0, column=1)

tk.Label(app, text='Include numbers?').grid(row=1, column=0)
tk.Checkbutton(app, variable=numbers_var).grid(row=1, column=1)

tk.Label(app, text='Password length (3-20):').grid(row=2, column=0)
length_entry = tk.Entry(app)
length_entry.grid(row=2, column=1)

submit_button = tk.Button(app, text='Generate Password', command=on_submit)
submit_button.grid(row=3, columnspan=2)

app.mainloop()
