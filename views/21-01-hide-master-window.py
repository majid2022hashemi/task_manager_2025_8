import tkinter as tk
from tkinter import ttk

# main window
window = tk.Tk()
window.geometry('600x400')
window.title('Main Window')

# function to hide main window and open new one
def open_new_window():
    window.withdraw()  # hides the main window

    new_win = tk.Toplevel()
    new_win.geometry('400x300')
    new_win.title('New Window')

    label = ttk.Label(new_win, text="This is the new window!")
    label.pack(pady=50)

    close_button = ttk.Button(new_win, text="Close", command=lambda: close_new_window(new_win))
    close_button.pack()

def close_new_window(new_win):
    new_win.destroy()
    window.deiconify()  # show main window again

# main UI
label = ttk.Label(window, text='A label')
label.pack(expand=True)

button = ttk.Button(window, text='Open New Window', command=open_new_window)
button.pack(side='bottom', fill='x')

# run
window.mainloop()
