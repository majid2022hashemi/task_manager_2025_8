import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from db import get_connection
import tkinter as tk  # Needed for tk.END

class AppWindow:
    def __init__(self, root):
        self.root = root
        self.top = ttk.Window(themename="flatly")
        self.top.geometry('1000x1000')
        self.top.title('App Task Manager')

        self.create_menu()
        self.create_layout()
        self.create_menu_widgets()
        self.create_table()
        self.load_data()

        self.top.mainloop()

    def create_menu(self):
        menu = ttk.Menu(self.top)

        file_menu = ttk.Menu(menu, tearoff=False)
        file_menu.add_command(label='New', command=lambda: print('New file'))
        file_menu.add_command(label='Open', command=lambda: print('Open file'))
        file_menu.add_command(label='Update', command=lambda: print('Update file'))
        file_menu.add_command(label='Delete', command=lambda: print('Delete file'))
        file_menu.add_separator()
        menu.add_cascade(label='File', menu=file_menu)

        self.help_check_string = ttk.StringVar()
        help_menu = ttk.Menu(menu, tearoff=False)
        help_menu.add_command(label='Help entry', command=lambda: print(self.help_check_string.get()))
        help_menu.add_checkbutton(label='check', onvalue='on', offvalue='off', variable=self.help_check_string)
        menu.add_cascade(label='Help', menu=help_menu)

        exercise_menu = ttk.Menu(menu, tearoff=False)
        exercise_menu.add_command(label='Open')
        exercise_sub_menu = ttk.Menu(menu, tearoff=False)
        exercise_sub_menu.add_command(label='some more stuff')
        exercise_menu.add_cascade(label='Change Profile', menu=exercise_sub_menu)
        menu.add_cascade(label='Profile', menu=exercise_menu)

        self.top.config(menu=menu)

    def create_layout(self):
        self.menu_frame = ttk.Frame(self.top)
        self.main_frame = ttk.Frame(self.top)

        self.menu_frame.place(x=0, y=0, relwidth=0.3, relheight=1)
        self.main_frame.place(relx=0.3, y=0, relwidth=0.7, relheight=1)

    def create_menu_widgets(self):
        menu_button1 = ttk.Button(self.menu_frame, text='Button 1')
        menu_button2 = ttk.Button(self.menu_frame, text='Button 2')
        menu_button3 = ttk.Button(self.menu_frame, text='Button 3')

        menu_slider1 = ttk.Scale(self.menu_frame, orient='vertical')
        menu_slider2 = ttk.Scale(self.menu_frame, orient='vertical')

        toggle_frame = ttk.Frame(self.menu_frame)
        menu_toggle1 = ttk.Checkbutton(toggle_frame, text='check 1')
        menu_toggle2 = ttk.Checkbutton(toggle_frame, text='check 2')

        entry = ttk.Entry(self.menu_frame)

        self.menu_frame.columnconfigure((0, 1, 2), weight=1, uniform='a')
        self.menu_frame.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        menu_button1.grid(row=0, column=0, sticky='nswe', columnspan=2, padx=4, pady=4)
        menu_button2.grid(row=0, column=2, sticky='nswe', padx=4, pady=4)
        menu_button3.grid(row=1, column=0, columnspan=3, sticky='nsew', padx=4, pady=4)

        menu_slider1.grid(row=2, column=0, rowspan=2, sticky='nsew', pady=20)
        menu_slider2.grid(row=2, column=2, rowspan=2, sticky='nsew', pady=20)

        toggle_frame.grid(row=4, column=0, columnspan=3, sticky='nsew')
        menu_toggle1.pack(side='left', expand=True)
        menu_toggle2.pack(side='left', expand=True)

        entry.place(relx=0.5, rely=0.95, relwidth=0.9, anchor='center')

    def create_table(self):
        self.columns = ('id', 'title', 'description', 'due_date', 'created_at', 'user_id', 'status_id', 'priority_id', 'duration_days')
        self.table = ttk.Treeview(self.main_frame, columns=self.columns, show='headings', selectmode='browse')

        for col in self.columns:
            self.table.heading(col, text=col.replace('_', ' ').title())
            self.table.column(col, width=100, anchor='center')

        self.table.tag_configure('evenrow', background='white')
        self.table.tag_configure('oddrow', background='lightgray')

        scrollbar = ttk.Scrollbar(self.main_frame, orient='vertical', command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side='left', expand=True, fill='both', padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)

    def load_data(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, title, description, due_date, created_at, user_id, status_id, priority_id, duration_days FROM tasks")
            rows = cur.fetchall()

            for i, row in enumerate(rows):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.table.insert('', tk.END, values=row, tags=(tag,))

            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error fetching data: {e}")
