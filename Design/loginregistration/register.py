from tkinter import *
from tkinter import messagebox
import subprocess
import sqlite3

# Colors
bgcolor = "#ffffff"  # Light gray
header_color = "#003366"  # Deep blue
frame_bg = "#e6e6e6"  # Gray
label_text_color = "#003366"  # Deep blue for text
tablecolor = '#00509e'

a = Tk()
a.title("Register")
a.attributes('-fullscreen', True)

def back_to_welcome():
    a.destroy()
    subprocess.Popen(["python", "welcome.py"])

def open_login():
    a.destroy()
    subprocess.Popen(["python", "login.py"])

def register_user():
    fullname = name_entry.get()
    username = user_entry.get()
    contact = contact_entry.get()
    email = email_entry.get()
    password = pass_entry.get()
    confirm_password = confirm_pass_entry.get()

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    try:
        conn = sqlite3.connect('quiz.db')  # Replace with your actual database name
        c = conn.cursor()
        c.execute("""
            INSERT INTO users (fullname, email, username, contact, password)
            VALUES (?, ?, ?, ?, ?)
        """, (fullname, email, username, contact, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Registration successful!")
        a.destroy()
        subprocess.Popen(["python", "userdashboard.py"])
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username or email already exists")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def adjust_frames(event=None):
    a.update_idletasks()
    window_width = a.winfo_width()
    window_height = a.winfo_height()

    if window_width > 700 or window_height > 400:
        x_main = (window_width - 500) // 2
        y_main = (window_height - 250) // 2
        button_x = window_width - 200
    else:
        x_main, y_main = 0, 0
        button_x = 500

    framemain.place(x=0, y=0, width=window_width, height=window_height)
    topframemain.place(x=0, y=0, width=window_width, height=25)
    welcomeframe.place(x=x_main+60, y=y_main - 80, width=400, height=60)
    frame.place(x=x_main, y=y_main, width=500, height=250)
    infotopframe.place(x=x_main, y=y_main, width=500, height=20)
    backframe.place(x=x_main + 450, y=y_main, width=50, height=20)
    register_button.place(x=button_x, y=30)
    login_button.place(x=button_x + 100, y=30)

a.bind("<Configure>", adjust_frames)

framemain = Frame(a, bd=2, relief="ridge", padx=0, pady=0, bg=bgcolor)
framemain.place(x=0, y=0, width=700, height=400)

topframemain = Frame(a, bd=2, relief="ridge", padx=0, pady=0, bg='#003366')
topframemain.place(x=0, y=0, width=700, height=25)
Label(topframemain, text="Quiz App", font=("Arial", 12), padx=20, pady=0, bg='#003366').place(x=0, y=0)

welcomeframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0, bg=tablecolor)
welcomeframe.place(x=150, y=70, width=400, height=60)
Label(welcomeframe, text="Welcome to Quiz App", font=("Arial", 30, "bold"), bg=tablecolor).pack(pady=10, padx=10)

frame = Frame(a, bd=2, relief="ridge", padx=20, pady=20, bg=bgcolor)
frame.place(x=100, y=140, width=500, height=250)

Label(frame, text="Name:", bg='white', fg='black').place(x=5, y=0)
name_entry = Entry(frame)
name_entry.place(x=5, y=20)

Label(frame, text="Username:", bg='white', fg='black').place(x=5, y=50)
user_entry = Entry(frame)
user_entry.place(x=5, y=70)

Label(frame, text="Contact Number:", bg='white', fg='black').place(x=5, y=100)
contact_entry = Entry(frame)
contact_entry.place(x=5, y=120)

Label(frame, text="E-mail:", bg='white', fg='black').place(x=5, y=150)
email_entry = Entry(frame)
email_entry.place(x=5, y=170)

Label(frame, text="Password:", bg='white', fg='black').place(x=250, y=0)
pass_entry = Entry(frame, show="*")
pass_entry.place(x=250, y=20)

Label(frame, text="Confirm Password:", bg='white', fg='black').place(x=250, y=50)
confirm_pass_entry = Entry(frame, show="*")
confirm_pass_entry.place(x=250, y=70)

Button(frame, text="Register", command=register_user, highlightbackground='white').place(x=200, y=190)

infotopframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0, bg='#003366')
infotopframe.place(x=100, y=140, width=500, height=20)
Label(infotopframe, text="Register", font=("Arial", 10), padx=15, pady=-2, bg='#003366').place(x=0, y=0)

backframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0, bg='black')
backframe.place(x=450, y=140, width=50, height=20)

# Use Label as a button
back_label = Label(
    backframe,
    text="Back",
    bg="black",
    fg="white",
    font=("Arial", 10),
)
back_label.place(x=0, y=-1)

# Bind a click event to the label
back_label.bind("<Button-1>", lambda e: back_to_welcome())

register_button = Button(framemain, text="Register", command=register_user, highlightbackground='white')
register_button.place(x=500, y=30)

login_button = Button(framemain, text="Login", command=open_login, highlightbackground='white')
login_button.place(x=600, y=30)

adjust_frames()
a.mainloop()