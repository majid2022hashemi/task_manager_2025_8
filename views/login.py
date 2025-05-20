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
        root.title("Login")
        root.geometry("400x500")
        root.configure(bg="#fff")
        root.resizable(False, False)

        # Frame container
        frame = ttk.Frame(root, width=360, height=380, bootstyle="light")
        frame.place(relx=0.5, rely=0.5, anchor='center')

        # Title
        ttk.Label(frame, text="Welcome", font=("Helvetica", 20, "bold"), bootstyle="dark").pack(pady=(20, 10))

        # Email Entry
        self.email_entry = ttk.Entry(frame, font=('Helvetica', 11), width=35, bootstyle="default")
        self.email_entry.insert(0, "Email or phone")
        self.email_entry.bind('<FocusIn>', self.clear_email_placeholder)
        self.email_entry.pack(pady=(10, 10))

        # Password Entry
        self.password_entry = ttk.Entry(frame, font=('Helvetica', 11), width=35, bootstyle="default", show='')
        self.password_entry.insert(0, "Enter your password")
        self.password_entry.bind('<FocusIn>', self.clear_password_placeholder)
        self.password_entry.pack(pady=(10, 5))

        # Show password checkbox
        self.show_password_var = tk.BooleanVar()
        show_checkbox = ttk.Checkbutton(frame, text="Show password", variable=self.show_password_var, command=self.toggle_password)
        show_checkbox.pack(anchor="w", padx=25)

        # Forgot password link
        ttk.Button(frame, text="Forgot password?", bootstyle="link", command=self.forgot_password).pack(anchor="w", padx=25, pady=(5, 20))

        # Sign-in button
        ttk.Button(frame, text="Next", width=30, bootstyle="primary", command=self.open_app).pack()

        # Create account link
        ttk.Button(frame, text="Create account", bootstyle="link", command=self.open_register).pack(pady=(20, 0))

    def clear_email_placeholder(self, event):
        if self.email_entry.get() == "Email or phone":
            self.email_entry.delete(0, tk.END)

    def clear_password_placeholder(self, event):
        if self.password_entry.get() == "Enter your password":
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(show="*")

    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

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


    def open_app(self):
        AppWindow(self.root)

    def open_register(self):
        RegisterWindow(self.root)

    def forgot_password(self):
        messagebox.showinfo("Forgot Password", "Password recovery is not implemented yet.")



# img_path = "path_to_image.png"
# img = ttk.PhotoImage(file=img_path)
# ttk.Label(frame, image=img).pack()
# self.img = img  # to prevent garbage collection
