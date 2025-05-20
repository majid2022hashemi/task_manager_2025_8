import tkinter as tk
from tkinter import messagebox
from db import get_connection
from app import AppWindow
from utils.security import check_password
from views.register import RegisterWindow
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x500")
        self.root.configure(bg="#fff")
        self.root.resizable(False, False)

        frame = ttk.Frame(root, width=360, height=380, bootstyle="light")
        frame.place(relx=0.5, rely=0.5, anchor='center')

        ttk.Label(frame, text="Welcome", font=("Helvetica", 20, "bold"), bootstyle="dark").pack(pady=(20, 10))

        self.email_entry = ttk.Entry(frame, font=('Helvetica', 11), width=35, bootstyle="default")
        self.email_entry.insert(0, "Email or phone")
        self.email_entry.bind('<FocusIn>', self.clear_email_placeholder)
        self.email_entry.pack(pady=(10, 10))

        self.password_entry = ttk.Entry(frame, font=('Helvetica', 11), width=35, bootstyle="default", show='')
        self.password_entry.insert(0, "Enter your password")
        self.password_entry.bind('<FocusIn>', self.clear_password_placeholder)
        self.password_entry.pack(pady=(10, 5))

        self.show_password_var = tk.BooleanVar()
        show_checkbox = ttk.Checkbutton(frame, text="Show password", variable=self.show_password_var, command=self.toggle_password)
        show_checkbox.pack(anchor="w", padx=25)

        ttk.Button(frame, text="Forgot password?", bootstyle="link", command=self.forgot_password).pack(anchor="w", padx=25, pady=(5, 20))

        # ✅ FIX: call self.login, not open_app
        ttk.Button(frame, text="Next", width=30, bootstyle="primary", command=self.login).pack()

        ttk.Button(frame, text="Create account", bootstyle="link", command=self.open_register).pack(pady=(20, 0))

    def clear_email_placeholder(self, event):
        if self.email_entry.get() == "Email or phone":
            self.email_entry.delete(0, tk.END)

    def clear_password_placeholder(self, event):
        if self.password_entry.get() == "Enter your password":
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(show="*")

    def toggle_password(self):
        self.password_entry.config(show="" if self.show_password_var.get() else "*")

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password, role FROM users WHERE email = %s", (email,))
        result = cur.fetchone()
        conn.close()

        if result:
            user_id, stored_password, role = result
            if check_password(password, stored_password):
                messagebox.showinfo("Login", f"Welcome {role}")
                self.open_app(user_id)
            else:
                messagebox.showerror("Error", "Incorrect password")
        else:
            messagebox.showerror("Error", "Email not found")

    # ✅ Now takes user_id
    def open_app(self, user_id):
        self.root.destroy()  # close login window
        AppWindow(user_id)   # pass user_id to app

    def open_register(self):
        RegisterWindow(self.root)

    def forgot_password(self):
        messagebox.showinfo("Forgot Password", "Password recovery is not implemented yet.")
