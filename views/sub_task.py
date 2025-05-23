import sys
import os
import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Treeview, Button, Label

# Add project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from db import get_connection

class SubTaskWindow:
    def __init__(self, window):
        self.window = window
        self.window.title('Sub Task Manager')
        self.window.geometry('1000x800')

        # Apply ttkbootstrap style
        self.style = Style("litera")

        # Load Button
        Button(self.window, text="Load Subtasks", command=self.load_data).pack(pady=10)

        # Treeview (created later after fetching columns)
        self.tree = None

    def load_data(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT title, description, is_completed, created_at FROM public.subtasks;")
            rows = cur.fetchall()

            # Get column names from cursor
            col_names = [desc[0] for desc in cur.description]

            # If tree already exists, destroy it and recreate
            if self.tree:
                self.tree.destroy()

            # Create Treeview with dynamic columns
            self.tree = Treeview(self.window, columns=col_names, show="headings")
            for col in col_names:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=150, anchor="center")
            self.tree.pack(fill="both", expand=True)

            # Insert rows
            for row in rows:
                self.tree.insert("", "end", values=row)

        except Exception as e:
            print(f"[ERROR] {e}")
            Label(self.window, text=f"Error loading subtasks: {e}", bootstyle="danger").pack()
        finally:
            if 'conn' in locals():
                conn.close()


def main():
    root = tk.Tk()
    app = SubTaskWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
