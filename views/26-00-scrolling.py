import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from random import randint, choice

# setup window using ttkbootstrap
window = ttk.Window(themename="flatly")  # You can use other themes like 'darkly', 'cosmo', etc.
window.geometry('600x400')
window.title('Scrolling')

# treeview
table = ttk.Treeview(window, columns=(1, 2), show='headings', selectmode='browse')
table.heading(1, text='First name')
table.heading(2, text='Last name')

# Define tag styles
table.tag_configure('evenrow', background='white')
table.tag_configure('oddrow', background='lightgray') 

# Sample data
first_names = ['Bob', 'Maria', 'Alex', 'James', 'Susan', 'Henry', 'Lisa', 'Anna', 'Lisa']
last_names = ['Smith', 'Brown', 'Wilson', 'Thomson', 'Cook', 'Taylor', 'Walker', 'Clark']

# Insert data with alternating row colors
for i in range(100):
    tag = 'evenrow' if i % 2 == 0 else 'oddrow'
    table.insert(parent='', index=END, values=(choice(first_names), choice(last_names)), tags=(tag,))

table.pack(expand=True, fill='both')

# Scrollbar
scrollbar_table = ttk.Scrollbar(window, orient='vertical', command=table.yview)
table.configure(yscrollcommand=scrollbar_table.set)
scrollbar_table.place(relx=1, rely=0, relheight=1, anchor='ne')

# run
window.mainloop()
