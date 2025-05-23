import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from utils.security import hash_password
from db.db import get_connection


class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.top = ctk.CTkToplevel(root)
        self.top.title("Create your account")
        self.top.geometry("500x500")
        self.top.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title_label = ctk.CTkLabel(self.top, text="Create a account", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        # First name
        self.name_entry = ctk.CTkEntry(self.top, placeholder_text="Full Name")
        self.name_entry.pack(pady=10, padx=50, fill="x")

        # Email
        self.email_entry = ctk.CTkEntry(self.top, placeholder_text="Email")
        self.email_entry.pack(pady=10, padx=50, fill="x")

        # Password
        self.password_entry = ctk.CTkEntry(self.top, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10, padx=50, fill="x")

        # Register button
        self.register_button = ctk.CTkButton(self.top, text="Next", command=self.register_user)
        self.register_button.pack(pady=20)

    def register_user(self):
        full_name = self.name_entry.get().strip()
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
            self.top.destroy()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to register user: {e}")
        finally:
            cur.close()
            conn.close()
