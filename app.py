import tkinter as tk
import urllib.request
from PIL import Image, ImageTk
import os
import io
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from db import get_connection
import tkinter.messagebox as messagebox 

class AppWindow:
    def __init__(self, window, user_id):
        self.window = window
        self.user_id = user_id
        self.selected_task_id = None
        self.window.title('App Task Manager')
        self.window.geometry('1000x700')

        self.create_menu()
        self.create_layout()
        self.create_menu_widgets()
        self.create_table()
        self.load_data()

    def create_menu(self):
        menu = ttk.Menu(self.window)
        menu.add_cascade(label='File', menu=ttk.Menu(menu, tearoff=False))
        menu.add_cascade(label='Help', menu=ttk.Menu(menu, tearoff=False))
        menu.add_cascade(label='Profile', menu=ttk.Menu(menu, tearoff=False))
        self.window.config(menu=menu)

    def create_layout(self):
        self.menu_frame = ttk.Frame(self.window)
        self.main_frame = ttk.Frame(self.window)

        self.menu_frame.place(x=0, y=0, relwidth=0.35, relheight=1)
        self.main_frame.place(relx=0.35, y=0, relwidth=0.65, relheight=1)

    def create_menu_widgets(self):
        avatar_path = self.get_user_avatar()

        try:
            if avatar_path:
                if avatar_path.startswith("http"):
                    with urllib.request.urlopen(avatar_path) as u:
                        raw_data = u.read()
                    image = Image.open(io.BytesIO(raw_data))
                else:
                    if not os.path.isabs(avatar_path):
                        avatar_path = os.path.join(os.path.dirname(__file__), avatar_path)
                    if not os.path.exists(avatar_path):
                        raise FileNotFoundError(f"File does not exist: {avatar_path}")
                    image = Image.open(avatar_path)

                image = image.resize((150, 150), Image.Resampling.LANCZOS)
                self.avatar_image = ImageTk.PhotoImage(image)
                ttk.Label(self.menu_frame, image=self.avatar_image).pack(pady=10)
            else:
                raise ValueError("No avatar path in database")
        except Exception as e:
            print(f"[ERROR] Could not load avatar image: {e}")
            ttk.Label(self.menu_frame, text='[No Image]').pack(pady=10)

        # Buttons
        ttk.Button(self.menu_frame, text='Insert', bootstyle="info", command=self.clear_form).pack(fill='x', padx=10, pady=5)
        ttk.Button(self.menu_frame, text='Edit', bootstyle="info", command=self.fill_form_from_selection).pack(fill='x', padx=10, pady=5)
        ttk.Button(self.menu_frame, text='Delete', bootstyle="danger", command=self.delete_task).pack(fill='x', padx=10, pady=5)

        # Form
        self.form_frame = ttk.Labelframe(self.menu_frame, text="Task Editor")
        self.form_frame.pack(fill='both', padx=10, pady=10, expand=True)

        self.title_entry = ttk.Entry(self.form_frame)
        self.desc_entry = ttk.Entry(self.form_frame)
        self.due_entry = ttk.Entry(self.form_frame)
        self.status_entry = ttk.Entry(self.form_frame)
        self.priority_entry = ttk.Entry(self.form_frame)

        ttk.Label(self.form_frame, text="Title").pack(anchor='w')
        self.title_entry.pack(fill='x')

        ttk.Label(self.form_frame, text="Description").pack(anchor='w')
        self.desc_entry.pack(fill='x')

        ttk.Label(self.form_frame, text="Due Date (YYYY-MM-DD)").pack(anchor='w')
        self.due_entry.pack(fill='x')

        ttk.Label(self.form_frame, text="Status ID").pack(anchor='w')
        self.status_entry.pack(fill='x')

        ttk.Label(self.form_frame, text="Priority ID").pack(anchor='w')
        self.priority_entry.pack(fill='x')

        ttk.Button(self.form_frame, text="Save", bootstyle="success", command=self.save_task).pack(pady=10)

    def get_user_avatar(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT avatar_url FROM user_profiles WHERE user_id = %s", (self.user_id,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            return result[0] if result and result[0] else ""
        except Exception as e:
            print(f"Error getting avatar: {e}")
            return ""

    def create_table(self):
        self.columns = (
            'id', 'title', 'description', 'due_date',
            'created_at', 'status_id', 'priority_id', 'duration_days'
        )
        self.table = ttk.Treeview(self.main_frame, columns=self.columns, show='headings')

        for col in self.columns:
            self.table.heading(col, text=col.replace('_', ' ').title())
            self.table.column(col, width=100, anchor='center')

        self.table.pack(expand=True, fill='both', padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self.main_frame, orient='vertical', command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

    def load_data(self):
        for row in self.table.get_children():
            self.table.delete(row)

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT id, title, description, due_date, created_at, status_id, priority_id, duration_days 
                FROM tasks WHERE user_id = %s
            """, (self.user_id,))
            rows = cur.fetchall()
            cur.close()
            conn.close()

            for i, row in enumerate(rows):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.table.insert('', tk.END, values=row, tags=(tag,))
        except Exception as e:
            print(f"Error loading tasks: {e}")

    def clear_form(self):
        self.selected_task_id = None
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)
        self.status_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)

    def fill_form_from_selection(self):
        selected = self.table.focus()
        if not selected:
            return

        values = self.table.item(selected, 'values')
        self.selected_task_id = values[0]
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, values[1])
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, values[2])
        self.due_entry.delete(0, tk.END)
        self.due_entry.insert(0, values[3])
        self.status_entry.delete(0, tk.END)
        self.status_entry.insert(0, values[5])
        self.priority_entry.delete(0, tk.END)
        self.priority_entry.insert(0, values[6])

    def save_task(self):
        title = self.title_entry.get()
        desc = self.desc_entry.get()
        due = self.due_entry.get()
        status = self.status_entry.get()
        priority = self.priority_entry.get()

        if not title:
            print("Title is required")
            return

        conn = get_connection()
        cur = conn.cursor()
        if self.selected_task_id:
            # Update existing task
            cur.execute("""
                UPDATE tasks SET title = %s, description = %s, due_date = %s,
                status_id = %s, priority_id = %s WHERE id = %s AND user_id = %s
            """, (title, desc, due, status, priority, self.selected_task_id, self.user_id))
        else:
            # Insert new task
            cur.execute("""
                INSERT INTO tasks (title, description, due_date, status_id, priority_id, user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (title, desc, due, status, priority, self.user_id))
        conn.commit()
        cur.close()
        conn.close()
        self.clear_form()
        self.load_data()



    def delete_task(self):
        selected = self.table.focus()
        if not selected:
            messagebox.showwarning("No selection", "Please select a task to delete.")
            return

        task_id = self.table.item(selected, 'values')[0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?")
        if not confirm:
            return

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, self.user_id))
            conn.commit()
            cur.close()
            conn.close()
            self.load_data()
            messagebox.showinfo("Deleted", "Task has been deleted.")
        except Exception as e:
            print(f"Error deleting task: {e}")
            messagebox.showerror("Error", "Failed to delete task.")

