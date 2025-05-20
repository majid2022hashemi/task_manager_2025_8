from tkinter import *
from tkinter import ttk

def button_func():
    print('a button was pressed')

def exercise_button_func():
    print('Hello')


# create a window
window = Tk()
window.title('wnidow and widgets')
window.geometry('800x700')


# ttk label
label = ttk.Label(master=window,text='this is a test')
label.pack()
 
#  tk.text
text = Text(master=window)
text.pack()

# ttk entry 
entry = ttk.Entry(master=window)
entry.pack()

# ttk button
button = ttk.Button(master=window,
                    text='A button', 
                    command= button_func )
button.pack()

# exercise_label
exercise_label = ttk.Label(master=window,text='my label')
exercise_label.pack()

 # exercise button
#  excercise_button
exercise_button = ttk.Button(master=window,
                             text='exercise button',
                             command=exercise_button_func)
exercise_button.pack()


# run
window.mainloop()