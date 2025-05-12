from tkinter import *
from views.login import LoginWindow

def main():
    root = Tk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
