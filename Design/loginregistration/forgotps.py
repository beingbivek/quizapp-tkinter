from tkinter import *
from tkinter import messagebox
import subprocess

def back_to_welcome():
    a.destroy()
    subprocess.Popen(["python", "welcome.py"])

def open_login():
    a.destroy()
    subprocess.Popen(["python", "login.py"])

def open_registration():
    a.destroy()
    subprocess.Popen(["python", "register.py"])

def forgot_pw():
    username_or_email = name_entry.get().strip()
    newpassword = user_entry.get().strip()

    if not username_or_email or not newpassword:
        messagebox.showerror("Error", "All fields are required")
        return

    if "@" in username_or_email:
        if "@" not in username_or_email or "." not in username_or_email:
            messagebox.showerror("Error", "Invalid email address")
            return
    else:
        if len(username_or_email) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters long")
            return

    if len(newpassword) < 6:
        messagebox.showerror("Error", "Password must be at least 6 characters long")
        return

    # Show success message with user details (masking password)
    user_info = f"Username/Email: {username_or_email}\nNew Password: {'*' * len(newpassword)}"
    messagebox.showinfo("Success", f"Password updated successfully!\n\n{user_info}")

a = Tk()
a.title("Forgot Password")
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

    x_frame = x_main + 200
    y_frame = y_main + 140

    x_back = x_main + 450
    y_back = y_main + 140

    framemain.place(x=x_main, y=y_main, width=700, height=400)
    topframemain.place(x=x_main, y=y_main, width=700, height=25)
    welcomeframe.place(x=x_welcome, y=y_welcome, width=400, height=60)
    frame.place(x=x_frame, y=y_frame, width=300, height=250)
    infotopframe.place(x=x_frame, y=y_frame, width=300, height=20)
    backframe.place(x=x_back, y=y_back, width=50, height=20)

a.bind("<Configure>", adjust_frames)

framemain = Frame(a, bd=2, relief="ridge", padx=0, pady=0)
framemain.place(x=0, y=0, width=700, height=400)

topframemain = Frame(a, bd=2, relief="ridge", padx=0, pady=0)
topframemain.place(x=0, y=0, width=700, height=25)
Label(topframemain, text="Quiz App", font=("Arial", 12), padx=20, pady=0).place(x=0, y=0)

welcomeframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0)
welcomeframe.place(x=150, y=70, width=400, height=60)
Label(welcomeframe, text="Welcome to Quiz App", font=("Arial", 30, "bold")).pack(pady=10, padx=10)

frame = Frame(a, bd=2, relief="ridge", padx=20, pady=20)
frame.place(x=200, y=140, width=300, height=250)

Label(frame, text="Email/Username:").place(x=5, y=0)
name_entry = Entry(frame)
name_entry.place(x=5, y=20)

Label(frame, text="New Password:").place(x=5, y=50)
user_entry = Entry(frame, show="*")
user_entry.place(x=5, y=70)

Button(frame, text="Update", command=forgot_pw).place(x=100, y=190)

infotopframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0)
infotopframe.place(x=200, y=140, width=300, height=20)
Label(infotopframe, text="Forgot Password", font=("Arial", 10), padx=15, pady=-2).place(x=0, y=0)

backframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0)
backframe.place(x=450, y=140, width=50, height=20)
Button(backframe, text="Back", command=open_login).place(x=-10, y=-8)

# Top buttons
Button(framemain, text="Register", command=open_registration).place(x=500, y=30)
Button(framemain, text="Login", command=open_login).place(x=600, y=30)

adjust_frames()
a.mainloop()
