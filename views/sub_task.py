import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Treeview, Button, Label
from db.db import get_connection

class SubTaskWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title('Sub Task Manager')
        self.window.geometry('800x600')

        # Apply style
        Style("litera")

        Button(self.window, text="Load Subtasks", command=self.load_data).pack(pady=10)
        self.tree = Treeview(self.window, columns=("title", "description", "completed", "created_at"), show="headings")
        for col in ("title", "description", "completed", "created_at"):
            self.tree.heading(col, text=col.title())
            self.tree.column(col, anchor="center")
        self.tree.pack(expand=True, fill="both")

    def load_data(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT title, description, is_completed AS completed, created_at FROM subtasks")
            rows = cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            if 'conn' in locals():
                conn.close()
