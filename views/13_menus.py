import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from random import choice
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import get_connection



/home/majid/My_project/python_task/db.py
# create window
window = ttk.Window(themename="flatly")
window.geometry('1000x1000')
window.title('App Task Manager')

# create menu
menu = ttk.Menu(window)

# File menu
file_menu = ttk.Menu(menu, tearoff=False)
file_menu.add_command(label='New', command=lambda: print('New file'))
file_menu.add_command(label='Open', command=lambda: print('Open file'))
file_menu.add_command(label='Update', command=lambda: print('Update file'))
file_menu.add_command(label='Delete', command=lambda: print('Delete file'))
file_menu.add_separator()
menu.add_cascade(label='File', menu=file_menu)

# Help menu
help_check_string = ttk.StringVar()
help_menu = ttk.Menu(menu, tearoff=False)
help_menu.add_command(label='Help entry', command=lambda: print(help_check_string.get()))
help_menu.add_checkbutton(label='check', onvalue='on', offvalue='off', variable=help_check_string)
menu.add_cascade(label='Help', menu=help_menu)

# Profile menu
exercise_menu = ttk.Menu(menu, tearoff=False)
exercise_menu.add_command(label='Open')
menu.add_cascade(label='Profile', menu=exercise_menu)

# Nested submenu
exercise_sub_menu = ttk.Menu(menu, tearoff=False)
exercise_sub_menu.add_command(label='some more stuff')
exercise_menu.add_cascade(label='Change Profile', menu=exercise_sub_menu)

window.config(menu=menu)

# main layout frames
menu_frame = ttk.Frame(window)
main_frame = ttk.Frame(window)

# layout placement
menu_frame.place(x=0, y=0, relwidth=0.3, relheight=1)
main_frame.place(relx=0.3, y=0, relwidth=0.7, relheight=1)

# --- MENU WIDGETS ---
menu_button1 = ttk.Button(menu_frame, text='Button 1')
menu_button2 = ttk.Button(menu_frame, text='Button 2')
menu_button3 = ttk.Button(menu_frame, text='Button 3')

menu_slider1 = ttk.Scale(menu_frame, orient='vertical')
menu_slider2 = ttk.Scale(menu_frame, orient='vertical')

toggle_frame = ttk.Frame(menu_frame)
menu_toggle1 = ttk.Checkbutton(toggle_frame, text='check 1')
menu_toggle2 = ttk.Checkbutton(toggle_frame, text='check 2')

entry = ttk.Entry(menu_frame)

# layout for menu_frame
menu_frame.columnconfigure((0, 1, 2), weight=1, uniform='a')
menu_frame.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

menu_button1.grid(row=0, column=0, sticky='nswe', columnspan=2, padx=4, pady=4)
menu_button2.grid(row=0, column=2, sticky='nswe', padx=4, pady=4)
menu_button3.grid(row=1, column=0, columnspan=3, sticky='nsew', padx=4, pady=4)

menu_slider1.grid(row=2, column=0, rowspan=2, sticky='nsew', pady=20)
menu_slider2.grid(row=2, column=2, rowspan=2, sticky='nsew', pady=20)

toggle_frame.grid(row=4, column=0, columnspan=3, sticky='nsew')
menu_toggle1.pack(side='left', expand=True)
menu_toggle2.pack(side='left', expand=True)

entry.place(relx=0.5, rely=0.95, relwidth=0.9, anchor='center')

# --- MAIN FRAME: Insert Scrolling Table ---
# Treeview setup
table = ttk.Treeview(main_frame, columns=(1, 2), show='headings', selectmode='browse')
table.heading(1, text='First name')
table.heading(2, text='Last name')

# Row styling
table.tag_configure('evenrow', background='white')
table.tag_configure('oddrow', background='lightgray')

# # Sample data
# first_names = ['Bob', 'Maria', 'Alex', 'James', 'Susan', 'Henry', 'Lisa', 'Anna']
# last_names = ['Smith', 'Brown', 'Wilson', 'Thomson', 'Cook', 'Taylor', 'Walker', 'Clark']

# for i in range(100):
#     tag = 'evenrow' if i % 2 == 0 else 'oddrow'
#     table.insert('', END, values=(choice(first_names), choice(last_names)), tags=(tag,))

# ==================================connect to db task=====================



# Treeview columns
columns = ('id', 'title', 'description', 'due_date', 'created_at', 'user_id', 'status_id', 'priority_id', 'duration_days')

# Treeview setup for tasks
table = ttk.Treeview(main_frame, columns=columns, show='headings', selectmode='browse')

# Set headings for all columns
for col in columns:
    table.heading(col, text=col.replace('_', ' ').title())
    table.column(col, width=100, anchor='center')

# Row styling
table.tag_configure('evenrow', background='white')
table.tag_configure('oddrow', background='lightgray')

# --- Fetch data from database ---
try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, due_date, created_at, user_id, status_id, priority_id, duration_days FROM tasks")
    rows = cur.fetchall()
    for i, row in enumerate(rows):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        table.insert('', END, values=row, tags=(tag,))
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error fetching data: {e}")

# Scrollbar setup
scrollbar_table = ttk.Scrollbar(main_frame, orient='vertical', command=table.yview)
table.configure(yscrollcommand=scrollbar_table.set)

# Layout of table and scrollbar
table.pack(side='left', expand=True, fill='both', padx=10, pady=10)
scrollbar_table.pack(side='right', fill='y', pady=10)

#  ==========end of ==================connect to db task=====================

# Scrollbar setup
scrollbar_table = ttk.Scrollbar(main_frame, orient='vertical', command=table.yview)
table.configure(yscrollcommand=scrollbar_table.set)

# Layout of table and scrollbar
table.pack(side='left', expand=True, fill='both', padx=10, pady=10)
scrollbar_table.pack(side='right', fill='y', pady=10)

# --- RUN APP ---
window.mainloop()
