from tkinter import *
from tkinter import messagebox
from db import get_connection
from utils.security import check_password
from views.register import RegisterWindow

class LoginWindow:
    def __init__(self, root):
        self.root = root
        root.title("Login")
        self.root.geometry("500x500")

        Label(root, text="Email").pack()
        self.email_entry = Entry(root)
        self.email_entry.pack()

        Label(root, text="Password").pack()
        self.password_entry = Entry(root, show='*')
        self.password_entry.pack()

        Button(root, text="Login", command=self.login).pack()
        Button(root, text="Register", command=self.open_register).pack()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT password, role FROM users WHERE email = %s", (email,))
        result = cur.fetchone()
        conn.close()

        if result:
            stored_password, role = result
            if check_password(password, stored_password):
                messagebox.showinfo("Login", f"Welcome {role}")
                # TODO: Open admin or user dashboard
            else:
                messagebox.showerror("Error", "Incorrect password")
        else:
            messagebox.showerror("Error", "Email not found")

    def open_register(self):
        RegisterWindow(self.root)


