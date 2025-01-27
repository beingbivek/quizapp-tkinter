from tkinter import *
from tkinter import messagebox
import subprocess

# Predefined admin code (change this as needed)
ADMIN_CODE = "12345"

def back_to_welcome():
    a.destroy()
    subprocess.Popen(["python", "welcome.py"])

def open_login():
    a.destroy()
    subprocess.Popen(["python", "login.py"])

def open_registration():
    a.destroy()
    subprocess.Popen(["python", "register.py"])

def admin_login():
    entered_code = admin_code_entry.get().strip()

    if not entered_code:
        messagebox.showerror("Error", "Admin code is required")
        return

    if entered_code == ADMIN_CODE:
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
    else:
        messagebox.showerror("Error", "Invalid admin code")

a = Tk()
a.title("Admin Login")
a.geometry('700x400')
a.resizable(1, 1)

framemain = Frame(a, bd=2, relief="ridge", padx=0, pady=0)  # main frame
framemain.place(x=0, y=0, width=700, height=400)

topframemain = Frame(a, bd=2, relief="ridge", padx=0, pady=0)  # top frame with title of app
topframemain.place(x=0, y=0, width=700, height=25)
Label(topframemain, text="Quiz App", font=("Arial", 12), padx=20, pady=0).place(x=0, y=0)

welcomeframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0)  # welcome to.. frame
welcomeframe.place(x=150, y=70, width=400, height=60)

Label(welcomeframe, text="Welcome to Quiz App", font=("Arial", 30, "bold")).pack(pady=10, padx=10)

frame = Frame(a, bd=2, relief="ridge", padx=20, pady=20)  # information frame
frame.place(x=200, y=140, width=300, height=250)

Label(frame, text="Enter Admin Code:").place(x=5, y=0)
admin_code_entry = Entry(frame, show="*")
admin_code_entry.place(x=5, y=20)

Button(frame, text="Login", command=admin_login).place(x=100, y=190)

infotopframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0)  # information top frame
infotopframe.place(x=200, y=140, width=300, height=20)
Label(infotopframe, text="Admin Login", font=("Arial", 10), padx=15, pady=-2).place(x=0, y=0)

backframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0)  # back frame
backframe.place(x=450, y=140, width=50, height=20)
Button(backframe, text="Back", command=open_login).place(x=-10, y=-8)

# Top buttons
Button(framemain, text="Register", command=open_registration).place(x=500, y=30)
Button(framemain, text="Login", command=open_login).place(x=600, y=30)

a.mainloop()
