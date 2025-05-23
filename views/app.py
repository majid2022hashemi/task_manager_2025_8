import tkinter as tk
import urllib.request
from PIL import Image, ImageTk
import os
import io
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from db.db import get_connection
import tkinter.messagebox as messagebox
from ttkbootstrap.widgets import DateEntry


class AppWindow:
    def __init__(self, window, user_id):
        self.window = window
        self.user_id = user_id
        self.selected_task_id = None
        self.window.title('App Task Manager')
        self.window.geometry('1000x1000')

        self.status_dict = self.get_status_dict()
        self.priority_dict = self.get_priority_dict()
        self.reverse_status_dict = {v: k for k, v in self.status_dict.items()}
        self.reverse_priority_dict = {v: k for k, v in self.priority_dict.items()}

        self.create_menu()
        self.create_layout()
        self.create_menu_widgets()
        self.create_table()
        self.load_data()

    def get_status_dict(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM status ORDER BY id")
            result = cur.fetchall()
            cur.close()
            conn.close()
            return {str(row[0]): row[1] for row in result}
        except Exception as e:
            print(f"[ERROR] Loading status: {e}")
            return {}

    def get_priority_dict(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, level FROM priority_levels ORDER BY id")
            result = cur.fetchall()
            cur.close()
            conn.close()
            return {str(row[0]): row[1] for row in result}
        except Exception as e:
            print(f"[ERROR] Loading priority: {e}")
            return {}

    def create_menu(self):
        menu = ttk.Menu(self.window)
        menu.add_cascade(label='File', menu=ttk.Menu(menu, tearoff=False))
        menu.add_cascade(label='Help', menu=ttk.Menu(menu, tearoff=False))
        subtask_menu = ttk.Menu(menu, tearoff=False)
        subtask_menu.add_command(label='Open Subtask Manager', command=self.open_subtask_window)
        menu.add_cascade(label='Subtask', menu=subtask_menu)

        self.window.config(menu=menu)
    def open_subtask_window(self):
        try:
            from views.sub_task import SubTaskWindow  # Adjust path if needed
            SubTaskWindow(self.window)
        except Exception as e:
            print(f"Failed to open SubTaskWindow: {e}")

    def create_layout(self):
        self.menu_frame = ttk.Frame(self.window)
        self.main_frame = ttk.Frame(self.window)
        self.menu_frame.place(x=0, y=0, relwidth=0.35, relheight=1)
        self.main_frame.place(relx=0.35, y=0, relwidth=0.65, relheight=1)

    def get_user_name(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT full_name FROM users WHERE id = %s", (self.user_id,))

       
            result = cur.fetchone()
            cur.close()
            conn.close()
            return result[0] if result else "Unknown User"
        except Exception as e:
            print(f"Name DB error: {e}")
            return "Unknown User"


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
                    image = Image.open(avatar_path)
                image = image.resize((150, 150), Image.Resampling.LANCZOS)
                self.avatar_image = ImageTk.PhotoImage(image)
                ttk.Label(self.menu_frame, image=self.avatar_image).pack(pady=10)
            else:
                raise ValueError("No avatar path")
        except Exception as e:
            print(f"Avatar error: {e}")
            ttk.Label(self.menu_frame, text='[No Image]').pack(pady=10)

        # Get and display user name
        user_name = 'User: ' + self.get_user_name()
        ttk.Label(self.menu_frame, text=user_name, font=('Helvetica', 12, 'bold')).pack(pady=(0, 10))

        ttk.Button(self.menu_frame, text='Insert', bootstyle="info", command=self.clear_form).pack(fill='x', padx=10, pady=5)
        ttk.Button(self.menu_frame, text='Edit', bootstyle="info", command=self.fill_form_from_selection).pack(fill='x', padx=10, pady=5)
        ttk.Button(self.menu_frame, text='Delete', bootstyle="danger", command=self.delete_task).pack(fill='x', padx=10, pady=5)

        self.form_frame = ttk.Labelframe(self.menu_frame, text="Task Editor")
        self.form_frame.pack(fill='both', padx=10, pady=10, expand=True)

        self.title_entry = ttk.Entry(self.form_frame)
        self.desc_entry = ttk.Entry(self.form_frame)
        self.due_entry = DateEntry(self.form_frame, dateformat="%Y-%m-%d")

        self.status_var = tk.StringVar()
        self.status_combobox = ttk.Combobox(self.form_frame, textvariable=self.status_var, state="readonly")
        self.status_combobox['values'] = list(self.status_dict.values())

        self.priority_var = tk.StringVar()
        self.priority_combobox = ttk.Combobox(self.form_frame, textvariable=self.priority_var, state="readonly")
        self.priority_combobox['values'] = list(self.priority_dict.values())

        for label, widget in [
            ("Title", self.title_entry),
            ("Description", self.desc_entry),
            ("Due Date (YYYY-MM-DD)", self.due_entry),
            ("Status", self.status_combobox),
            ("Priority", self.priority_combobox)
        ]:
            ttk.Label(self.form_frame, text=label).pack(anchor='w')
            widget.pack(fill='x')

        ttk.Button(self.form_frame, text="Save", bootstyle="success", command=self.save_task).pack(pady=10)
        self.cancel_button = ttk.Button(self.form_frame, text="Cancel", bootstyle="secondary", command=self.clear_form)
        self.cancel_button.pack(pady=5)
        self.cancel_button.config(state=tk.DISABLED)

        for widget in [self.title_entry, self.desc_entry, self.due_entry.entry,
                       self.status_combobox, self.priority_combobox]:
            widget.bind("<KeyRelease>", self.update_cancel_button_state)
            widget.bind("<<ComboboxSelected>>", self.update_cancel_button_state)

    def update_cancel_button_state(self, event=None):
        fields = [
            self.title_entry.get().strip(),
            self.desc_entry.get().strip(),
            self.due_entry.entry.get().strip(),
            self.status_var.get().strip(),
            self.priority_var.get().strip(),
        ]
        if any(fields):
            self.cancel_button.config(state=tk.NORMAL)
        else:
            self.cancel_button.config(state=tk.DISABLED)

    def get_user_avatar(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT avatar_url FROM user_profiles WHERE user_id = %s", (self.user_id,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            return result[0] if result else ""
        except Exception as e:
            print(f"Avatar DB error: {e}")
            return ""

    def create_table(self):
        self.columns = (
            'id', 'title', 'description', 'due_date',
            'created_at', 'status', 'priority', 'duration_days'
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
                task_id, title, desc, due, created, status_id, priority_id, duration = row
                status_label = self.status_dict.get(str(status_id), status_id)
                priority_label = self.priority_dict.get(str(priority_id), priority_id)
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.table.insert('', tk.END, values=(
                    task_id, title, desc, due, created, status_label, priority_label, duration
                ), tags=(tag,))
        except Exception as e:
            print(f"Load error: {e}")

    def clear_form(self):
        self.selected_task_id = None
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.due_entry.entry.delete(0, tk.END)
        self.status_combobox.set("")
        self.priority_combobox.set("")
        self.update_cancel_button_state()

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
        self.due_entry.entry.delete(0, tk.END)
        self.due_entry.entry.insert(0, values[3])
        self.status_combobox.set(values[5])
        self.priority_combobox.set(values[6])
        self.update_cancel_button_state()

    def save_task(self):
        title = self.title_entry.get()
        desc = self.desc_entry.get()
        due = self.due_entry.entry.get()
        status_name = self.status_var.get()
        priority_name = self.priority_var.get()
        status = self.reverse_status_dict.get(status_name)
        priority = self.reverse_priority_dict.get(priority_name)

        if not title:
            messagebox.showwarning("Missing Title", "Title is required.")
            return

        try:
            conn = get_connection()
            cur = conn.cursor()
            if self.selected_task_id:
                cur.execute("""
                    UPDATE tasks SET title = %s, description = %s, due_date = %s,
                    status_id = %s, priority_id = %s WHERE id = %s AND user_id = %s
                """, (title, desc, due, status, priority, self.selected_task_id, self.user_id))
            else:
                cur.execute("""
                    INSERT INTO tasks (title, description, due_date, status_id, priority_id, user_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (title, desc, due, status, priority, self.user_id))

            conn.commit()
            cur.close()
            conn.close()
            self.clear_form()
            self.load_data()
            messagebox.showinfo("Success", "Task saved successfully.")
        except Exception as e:
            print(f"Save error: {e}")
            messagebox.showerror("Database Error", "Failed to save task.")

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
            print(f"Delete error: {e}")
            messagebox.showerror("Error", "Failed to delete task.")
