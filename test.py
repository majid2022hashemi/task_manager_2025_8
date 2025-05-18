import tkinter as tk
from tkinter import messagebox
import re  # For email validation
import os

class RegistrationForm:
    def __init__(self, root):
        self.root = root
        root.title("Registration Form")
        root.geometry("1000x1000+300+200")
        root.configure(bg="#fff")
        root.resizable(False, False)

        # Image (same style as login)

       
        img_path = os.path.join(os.path.dirname(__file__), "image/login.png")
        self.img = tk.PhotoImage(file=img_path)
        
        tk.Label(root, image=self.img, bg='white').place(x=50, y=50)

        # Frame container
        frame = tk.Frame(root, width=350, height=400, bg='white')
        frame.place(x=480, y=50)

        # Title
        heading = tk.Label(frame, text='Create Account', fg='#57a1f8', bg='white',
                         font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=60, y=5)

        # Form fields
        self._create_field(frame, "Username", 80)
        self._create_field(frame, "Email", 140)
        self._create_field(frame, "Phone", 200)
        self._create_password_field(frame, "Password", 260)
        self._create_password_field(frame, "Confirm Password", 320)

        # Terms checkbox
        self.terms_var = tk.IntVar()
        terms = tk.Checkbutton(frame, text="I agree to Terms & Conditions", variable=self.terms_var,
                             bg='white', font=('Microsoft YaHei UI Light', 9))
        terms.place(x=30, y=380)

        # Register button
        tk.Button(frame, width=39, text='Register', border=0, bg='#57a1f8', cursor='hand2',
                command=self._validate_form).place(x=35, y=410)

    def _create_field(self, parent, placeholder, y_pos):
        entry = tk.Entry(parent, width=25, fg='black', border=0, bg='white',
                        font=('Microsoft YaHei UI Light', 11))
        entry.place(x=30, y=y_pos)
        entry.insert(0, placeholder)
        entry.bind('<FocusIn>', lambda e: self._on_entry_click(e, placeholder))
        entry.bind('<FocusOut>', lambda e: self._on_focusout(e, placeholder))
        
        tk.Frame(parent, width=295, height=2, bg='black').place(x=25, y=y_pos+27)
        return entry

    def _create_password_field(self, parent, placeholder, y_pos):
        entry = tk.Entry(parent, width=25, fg='black', border=0, bg='white',
                        font=('Microsoft YaHei UI Light', 11), show='*')
        entry.place(x=30, y=y_pos)
        entry.insert(0, placeholder)
        entry.bind('<FocusIn>', lambda e: self._on_entry_click(e, placeholder))
        entry.bind('<FocusOut>', lambda e: self._on_focusout(e, placeholder))
        
        tk.Frame(parent, width=295, height=2, bg='black').place(x=25, y=y_pos+27)
        return entry

    def _on_entry_click(self, event, placeholder):
        entry = event.widget
        if entry.get() == placeholder:
            entry.delete(0, "end")
            if placeholder.lower().startswith('password'):
                entry.config(show='*')

    def _on_focusout(self, event, placeholder):
        entry = event.widget
        if entry.get() == '':
            entry.insert(0, placeholder)
            if placeholder.lower().startswith('password'):
                entry.config(show='')

    def _validate_form(self):
        # Get all form data (in a real app, you'd reference your Entry widgets)
        username = "test"  # Would get from Entry widget
        email = "test@example.com"
        phone = "1234567890"
        password = "password123"
        confirm_password = "password123"

        # Validation checks
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messagebox.showerror("Error", "Invalid email format")
            return

        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords don't match")
            return

        if not self.terms_var.get():
            messagebox.showerror("Error", "You must accept the terms")
            return

        # If all validations pass
        messagebox.showinfo("Success", "Registration successful!")
        # Here you would typically hash the password and save to database
        # self._save_to_database(username, email, phone, password)

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistrationForm(root)
    root.mainloop()