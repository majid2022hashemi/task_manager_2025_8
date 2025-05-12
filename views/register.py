import tkinter as tk
from tkinter import messagebox
from utils.security import hash_password
from db import get_connection

class RegisterWindow:
    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.title("Register")
        self.master.geometry("300x300")


       # Labels and Entries
        tk.Label(self.top, text="Full Name").pack()
        self.full_name_entry = tk.Entry(self.top)
        self.full_name_entry.pack()

        tk.Label(self.top, text="Email").pack()
        self.email_entry = tk.Entry(self.top)
        self.email_entry.pack()

        tk.Label(self.top, text="Password").pack()
        self.password_entry = tk.Entry(self.top, show='*')
        self.password_entry.pack()

         # Register Button
        tk.Button(self.top, text="Register", command=self.register_user).pack()


    def register_user(self):
        full_name = self.full_name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        if not full_name or not email or not password:
            messagebox.showerror("Error", "All fields are required.")
            return



        username = full_name.replace(" ", "_")
        hashed_pw = hash_password(password)



        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO users (username, email, password, full_name, role, is_active, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
            """, (username, email, hashed_pw, full_name, 'user', True))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            self.master.destroy()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to register user: {e}")
        finally:
            cur.close()
            conn.close()
