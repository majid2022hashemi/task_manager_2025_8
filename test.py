import ttkbootstrap as ttk
from ttkbootstrap.widgets import DateEntry
from datetime import datetime

# Create window
window = ttk.Window(themename='darkly')
window.title('Date Picker')
window.geometry("300x150")

# Calendar with YYYY-MM-DD formatting
calendar = DateEntry(window, dateformat='%Y-%m-%d')  # <- set display format
calendar.pack(pady=10)

# Button to get selected date
def show_selected_date():
    date = calendar.entry.get()
    try:
        # Validate format
        datetime.strptime(date, '%Y-%m-%d')
        print("Selected date:", date)
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")

ttk.Button(window, text='Get Calendar Date', command=show_selected_date).pack()

# Run app
window.mainloop()
