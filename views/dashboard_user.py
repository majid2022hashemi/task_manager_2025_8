# views/dashboard_user.py

import tkinter as tk
from tkinter import messagebox
import psycopg2
from db.db import get_connection

class UserDashboard(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.title(f"User Dashboard - {user['username']}")
        self.geometry("600x400")
        self.user = user

        tk.Label(self, text="User Dashboard", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="My Tasks", command=self.view_tasks).pack(pady=5)
        tk.Button(self, text="My Projects", command=self.view_projects).pack(pady=5)

    def view_tasks(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT title, description, due_date
            FROM tasks
            WHERE user_id = %s
            ORDER BY due_date;
        """, (self.user['id'],))
        tasks = cur.fetchall()
        cur.close()
        conn.close()

        task_str = "\n".join([f"{t[0]} - {t[1]} (Due: {t[2]})" for t in tasks])
        messagebox.showinfo("My Tasks", task_str or "No tasks found.")

    def view_projects(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT name, description
            FROM projects
            WHERE owner_id = %s;
        """, (self.user['id'],))
        projects = cur.fetchall()
        cur.close()
        conn.close()

        project_str = "\n".join([f"{p[0]} - {p[1]}" for p in projects])
        messagebox.showinfo("My Projects", project_str or "No projects found.")
