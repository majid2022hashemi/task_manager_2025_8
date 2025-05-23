# views/dashboard_admin.py

import tkinter as tk
from tkinter import messagebox
import psycopg2
from db.db import get_connection

class AdminDashboard(tk.Tk):
    def __init__(self, admin_user):
        super().__init__()
        self.title(f"Admin Dashboard - {admin_user['username']}")
        self.geometry("600x400")
        self.admin_user = admin_user

        tk.Label(self, text="Admin Dashboard", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="View All Users", command=self.view_users).pack(pady=5)
        tk.Button(self, text="View All Projects", command=self.view_projects).pack(pady=5)

    def view_users(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, email, role FROM users WHERE is_active = TRUE;")
        users = cur.fetchall()
        cur.close()
        conn.close()

        users_str = "\n".join([f"{u[0]}: {u[1]} ({u[2]}) - {u[3]}" for u in users])
        messagebox.showinfo("All Users", users_str or "No users found.")

    def view_projects(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, description FROM projects;")
        projects = cur.fetchall()
        cur.close()
        conn.close()

        projects_str = "\n".join([f"{p[0]}: {p[1]} - {p[2]}" for p in projects])
        messagebox.showinfo("All Projects", projects_str or "No projects found.")
