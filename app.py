import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from db import get_connection
import tkinter as tk

class AppWindow:
    def __init__(self, window, user_id):
        self.window = window
        self.user_id = user_id
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
        ttk.Button(self.menu_frame, text='Button 1').pack(fill='x', padx=10, pady=5)
        ttk.Button(self.menu_frame, text='Button 2').pack(fill='x', padx=10, pady=5)
        ttk.Button(self.menu_frame, text='Button 3').pack(fill='x', padx=10, pady=5)

    def create_table(self):
        self.columns = ('id', 'title', 'description', 'due_date', 'created_at', 'status_id', 'priority_id', 'duration_days')
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
            print(f"Error loading tasks: {e}")
