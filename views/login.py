from tkinter import *
from tkinter import messagebox
from db import get_connection
from utils.security import check_password
from views.register import RegisterWindow
import os

class LoginWindow:
    def __init__(self, root):
        self.root = root
        root.title("Login")
        root.geometry("925x500+300+200")
        root.configure(bg="#fff")
        root.resizable(False, False)

        # Dynamically resolve path to image
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../image/login.png"))
        self.img = PhotoImage(file=image_path)
        Label(root, image=self.img, bg='white').place(x=50, y=50)


        frame = Frame(root, width=350, height=350, bg='white')
        frame.place(x=480, y=70)

        heading = Label(frame, text='Sign in', fg='#57a1f8', bg='white',font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=100, y=5)
        

        # self.email_entry = Entry(frame, width=25, fg='black',border=0, bg='white',font=('Microsoft YaHeI UI Light',11))
        # self.email_entry .place(x=30,y=80)
        # self.email_entry .insert(0,"Email or phone")



        def on_entry_click(event):
            if self.email_entry.get() == "Email or phone":
                self.email_entry.delete(0, "end")  # delete all the text in the entry
                self.email_entry.config(fg='black')  # change text color to black

        def on_focusout(event):
            if self.email_entry.get() == "":
                self.email_entry.insert(0, "Email or phone")
                self.email_entry.config(fg='grey')  # change text color to grey

       # Create your entry widget
        self.email_entry = Entry(frame, width=25, fg='grey', border=0, bg='white', 
                                font=('Microsoft YaHeI UI Light', 11))
        self.email_entry.insert(0, "Email or phone")
        self.email_entry.place(x=30, y=80)

        # Add bindings for focus in/out
        self.email_entry.bind('<FocusIn>', on_entry_click)
        self.email_entry.bind('<FocusOut>', on_focusout)

      

        

        Frame(frame, width=250, height=2, bg='black').place(x=30, y=107)



        self.password_entry = Entry(frame, width=25, fg='black',border=0, bg='white',show='*' ,font=('Microsoft YaHeI UI Light',11))
        self.password_entry.place(x=30,y=150)
        self.password_entry.insert(0,"Password")

        Frame(frame,width=260, height=2, bg='black').place(x=25,y=177)


        # Button(frame,width=6,text='Sign in',border=0,bg='#57a1f8',command=self.login).place(x=35, y=204)

        next_button = Button(frame, width=15, pady=7, text='Sign in', bg='#1a73e8', fg='white', border=0, command=self.login,
                    font=('Microsoft YaHeI UI Light', 11, 'bold'))
        next_button.place(x=35, y=204)

        lable = Label(frame,text="Don't have an account?",fg='black',bg='white',font=('Microsoft YaHei UI Light',9))
        lable.place(x=75,y=270)
        register = Button(frame,width=12,text='Create Account',border=0,bg='white',cursor='hand2',fg='#57a1f8',command=self.open_register)
        register.place(x=215, y=270)  

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT password, role FROM users WHERE email = %s", (email,))
        result = cur.fetchone()
        conn.close()

        if result:
            stored_password, role = result
            if check_password(password, stored_password):
                messagebox.showinfo("Login", f"Welcome {role}")
                # TODO: Open admin or user dashboard
            else:
                messagebox.showerror("Error", "Incorrect password")
        else:
            messagebox.showerror("Error", "Email not found")

    def open_register(self):
        RegisterWindow(self.root)








        

