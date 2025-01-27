from tkinter import *
from tkinter import messagebox
import subprocess

a = Tk()
a.title("Register")
a.geometry('700x400')
a.resizable(1, 1)

def adjust_frames(event=None):
    a.update_idletasks()
    
    window_width = a.winfo_width()
    window_height = a.winfo_height()
    
    if window_width > 700 or window_height > 400:
        x_main = (window_width - 700) // 2
        y_main = (window_height - 400) // 2
    else:
        x_main, y_main = 0, 0

    x_welcome = x_main + 150
    y_welcome = y_main + 70

    x_frame = x_main + 100
    y_frame = y_main + 140

    x_back = x_main + 550
    y_back = y_main + 140

    framemain.place(x=x_main, y=y_main, width=700, height=400)
    topframemain.place(x=x_main, y=y_main, width=700, height=25)
    welcomeframe.place(x=x_welcome, y=y_welcome, width=400, height=60)
    frame.place(x=x_frame, y=y_frame, width=500, height=250)
    infotopframe.place(x=x_frame, y=y_frame, width=500, height=20)
    backframe.place(x=x_back, y=y_back, width=50, height=20)

a.bind("<Configure>", adjust_frames)

framemain = Frame(a, bd=2, relief="ridge", padx=0, pady=0)
framemain.place(x=0, y=0, width=700, height=400)

topframemain = Frame(a, bd=2, relief="ridge", padx=0, pady=0)
topframemain.place(x=0, y=0, width=700, height=25)
Label(topframemain, text="Quiz App", font=("Arial", 12), padx=20, pady=0).place(x=0, y=0)

def back_to_welcome():
    a.destroy()
    subprocess.Popen(["python", "welcome.py"])

def open_login():
    a.destroy()
    subprocess.Popen(["python", "login.py"])

def open_registration():
    a.destroy()
    subprocess.Popen(["python", "register.py"])

def register():
    name = name_entry.get().strip()
    username = user_entry.get().strip()
    contact = contact_entry.get().strip()
    email = email_entry.get().strip()
    password = pass_entry.get().strip()
    confirm_password = confirm_pass_entry.get().strip()

    if not name or not username or not contact or not email or not password or not confirm_password:
        messagebox.showerror("Error", "All fields are required")
        return

    if not contact.isdigit() or len(contact) != 10:
        messagebox.showerror("Error", "Contact number must be exactly 10 digits")
        return

    if "@" not in email or "." not in email:
        messagebox.showerror("Error", "Invalid email address")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    if len(username) < 3:
        messagebox.showerror("Error", "Username must be at least 3 characters long")
        return

    if len(password) < 6:
        messagebox.showerror("Error", "Password must be at least 6 characters long")
        return

    user_info = f"Name: {name}\nUsername: {username}\nContact: {contact}\nEmail: {email}"
    messagebox.showinfo("Registration Successful", f"You have been registered successfully!\n\n{user_info}")

welcomeframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0)
welcomeframe.place(x=150, y=70, width=400, height=60)
Label(welcomeframe, text="Welcome to Quiz App", font=("Arial", 30, "bold")).pack(pady=10, padx=10)

frame = Frame(a, bd=2, relief="ridge", padx=20, pady=20)
frame.place(x=100, y=140, width=500, height=250)

Label(frame, text="Name:").place(x=5, y=0)
name_entry = Entry(frame)
name_entry.place(x=5, y=20)

Label(frame, text="Username:").place(x=5, y=50)
user_entry = Entry(frame)
user_entry.place(x=5, y=70)

Label(frame, text="Contact Number:").place(x=5, y=100)
contact_entry = Entry(frame)
contact_entry.place(x=5, y=120)

Label(frame, text="E-mail:").place(x=5, y=150)
email_entry = Entry(frame)
email_entry.place(x=5, y=170)

Label(frame, text="Password:").place(x=250, y=0)
pass_entry = Entry(frame, show="*")
pass_entry.place(x=250, y=20)

Label(frame, text="Confirm Password:").place(x=250, y=50)
confirm_pass_entry = Entry(frame, show="*")
confirm_pass_entry.place(x=250, y=70)

Button(frame, text="Register", command=register).place(x=200, y=190)

infotopframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0)
infotopframe.place(x=100, y=140, width=500, height=20)
Label(infotopframe, text="Register", font=("Arial", 10), padx=15, pady=-2).place(x=0, y=0)

backframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0)
backframe.place(x=550, y=140, width=50, height=20)
Button(backframe, text="Back", command=back_to_welcome).place(x=-10, y=-8)

Button(framemain, text="Register", command=open_registration).place(x=500, y=30)
Button(framemain, text="Login", command=open_login).place(x=600, y=30)

adjust_frames()
a.mainloop()
