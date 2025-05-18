import tkinter as tk

def on_entry_focus_in(event):
    if email_entry.get() == "Email or phone":
        email_entry.delete(0, tk.END)
        email_entry.config(fg='black')
    # Activate blue underline (Google's focus effect)
    underline.config(bg='#1a73e8', height=2)

def on_entry_focus_out(event):
    if email_entry.get() == "":
        email_entry.insert(0, "Email or phone")
        email_entry.config(fg='#5f6368')  # Google's placeholder gray
    # Revert to gray underline
    underline.config(bg='#dadce0', height=1)

# Create window
root = tk.Tk()
root.geometry("350x200")
root.config(bg='white')

# Email Entry Frame (for padding)
entry_frame = tk.Frame(root, bg='white')
entry_frame.pack(pady=40)

# Entry Widget (no visible border)
email_entry = tk.Entry(
    entry_frame, 
    width=25, 
    fg='#5f6368',  # Google's placeholder gray
    border=0,
    bg='white',
    font=('Roboto', 11)  # Google's font (use 'Segoe UI' on Windows)
)
email_entry.pack()
email_entry.insert(0, "Email or phone")

# Underline (mimics Google's animated border)
underline = tk.Frame(
    entry_frame, 
    height=1, 
    bg='#dadce0'  # Google's default underline gray
)
underline.pack(fill='x')

# Next Button (Google's blue button)
next_button = tk.Button(
    root,
    text="Next",
    bg='#1a73e8',  # Google blue
    fg='white',
    font=('Roboto', 11, 'bold'),
    borderwidth=0,
    width=8
)
next_button.pack(pady=10)

# Bind focus events
email_entry.bind('<FocusIn>', on_entry_focus_in)
email_entry.bind('<FocusOut>', on_entry_focus_out)

root.mainloop()