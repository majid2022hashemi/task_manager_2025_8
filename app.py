import tkinter as tk
import urllib.request
from PIL import Image, ImageTk
import os
import io
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from db import get_connection

class AppWindow:
    def __init__(self, window, user_id):
        self.window = window
        self.user_id = user_id
        self.avatar_image = None  # Cache avatar image
        self.window.title('App Task Manager')
        self.window.geometry('1000x1000')

        self.create_menu()
        self.create_layout()
        self.create_menu_widgets()
        self.create_table()
        self.load_data()

    def create_menu(self):
        menu = ttk.Menu(self.window)

        file_menu = ttk.Menu(menu, tearoff=False)
        file_menu.add_command(label='New', command=lambda: print('New file'))
        file_menu.add_command(label='Open', command=lambda: print('Open file'))
        file_menu.add_command(label='Update', command=lambda: print('Update file'))
        file_menu.add_command(label='Delete', command=lambda: print('Delete file'))
        file_menu.add_separator()
        menu.add_cascade(label='File', menu=file_menu)

        help_menu = ttk.Menu(menu, tearoff=False)
        help_menu.add_command(label='Help entry')
        menu.add_cascade(label='Help', menu=help_menu)

        profile_menu = ttk.Menu(menu, tearoff=False)
        profile_menu.add_command(label='Change Profile')
        menu.add_cascade(label='Profile', menu=profile_menu)

        self.window.config(menu=menu)

    def create_layout(self):
        self.menu_frame = ttk.Frame(self.window)
        self.main_frame = ttk.Frame(self.window)

        self.menu_frame.place(x=0, y=0, relwidth=0.3, relheight=1)
        self.main_frame.place(relx=0.3, y=0, relwidth=0.7, relheight=1)




    def create_menu_widgets(self):
        # Avatar
        avatar_path = self.get_user_avatar()
        try:
            if avatar_path:
                if not os.path.isabs(avatar_path):
                    avatar_path = os.path.join(os.path.dirname(__file__), avatar_path)
                image = Image.open(avatar_path)
                image = image.resize((100, 100), Image.Resampling.LANCZOS)
                self.avatar_image = ImageTk.PhotoImage(image)
                ttk.Label(self.menu_frame, image=self.avatar_image).pack(pady=10)
        except Exception as e:
            print(f"[ERROR] Avatar load failed: {e}")
            ttk.Label(self.menu_frame, text="[No Avatar]").pack(pady=10)

        # Buttons
        ttk.Button(self.menu_frame, text='Insert', bootstyle="info", command=self.insert_task).pack(fill='x', padx=10, pady=5)
        ttk.Button(self.menu_frame, text='Edit', bootstyle="info", command=self.edit_task).pack(fill='x', padx=10, pady=5)
        ttk.Button(self.menu_frame, text='Delete', bootstyle="info", command=self.delete_task).pack(fill='x', padx=10, pady=5)

        # Spacer
        ttk.Label(self.menu_frame, text="").pack(expand=True, fill='both')

    def insert_task(self):
        self.open_task_editor()

    def edit_task(self):
        selected = self.table.selection()
        if not selected:
            tk.messagebox.showwarning("Warning", "Select a task to edit.")
            return
        values = self.table.item(selected[0], 'values')
        self.open_task_editor(task_data=values)

    def delete_task(self):
        selected = self.table.selection()
        if not selected:
            tk.messagebox.showwarning("Warning", "Select a task to delete.")
            return
        task_id = self.table.item(selected[0], 'values')[0]
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, self.user_id))
        conn.commit()
        cur.close()
        conn.close()
        self.load_data()

    def open_task_editor(self, task_data=None):
        editor = tk.Toplevel(self.window)
        editor.title("Task Editor")
        editor.geometry("400x400")

        fields = ['Title', 'Description', 'Due Date (YYYY-MM-DD)', 'Status ID', 'Priority ID', 'Duration (days)']
        entries = []

        for field in fields:
            ttk.Label(editor, text=field).pack(pady=5)
            entry = ttk.Entry(editor)
            entry.pack(fill='x', padx=10)
            entries.append(entry)

        if task_data:
            for i, entry in enumerate(entries):
                entry.insert(0, task_data[i+1])  # skip ID

        def save_task():
            values = [e.get().strip() for e in entries]
            if not all(values):
                tk.messagebox.showerror("Error", "All fields required.")
                return

            conn = get_connection()
            cur = conn.cursor()

            if task_data:
                cur.execute("""
                    UPDATE tasks SET title=%s, description=%s, due_date=%s, status_id=%s, priority_id=%s, duration_days=%s
                    WHERE id=%s AND user_id=%s
                """, (*values, task_data[0], self.user_id))
            else:
                cur.execute("""
                    INSERT INTO tasks (user_id, title, description, due_date, status_id, priority_id, duration_days)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (self.user_id, *values))

            conn.commit()
            cur.close()
            conn.close()
            self.load_data()
            editor.destroy()

        ttk.Button(editor, text="Save", bootstyle="success", command=save_task).pack(pady=20)





       
    def get_user_avatar(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT avatar_url FROM user_profiles WHERE user_id = %s", (self.user_id,))
            result = cur.fetchone()
            cur.close()
            conn.close()

            if result and result[0]:
                print(f"[DEBUG] Avatar path for user {self.user_id}: {result[0]}")
                return result[0]
        except Exception as e:
            print(f"[ERROR] Failed to retrieve avatar: {e}")
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
            print(f"[ERROR] Failed to load tasks: {e}")
