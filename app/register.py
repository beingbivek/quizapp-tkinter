from tkinter import *
from tkinter import messagebox
import sqlite3
import runpy
import tkinter.font as font
import pybase64  
import re

# Colors
bgcolor = "#E0E0E0"
header_color = "#34495E"
frame_bg = "#E0E0E0" 
button_color = '#1F618D'
tablecolor = '#34495E'

register = Tk()
register.title("Register")
register.attributes('-fullscreen', True)

from quizdefaults import *


def register_user():
    # Get input values
    fullname = name_entry.get().strip()
    username = user_entry.get().strip()
    contact = contact_entry.get().strip()
    email = email_entry.get().strip()
    password = pass_entry.get().strip()
    confirm_password = confirm_pass_entry.get().strip()

    if not (fullname and username and contact and email and password and confirm_password):
        messagebox.showerror("Error", "Please fill all the fields!")
        return

    
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", username):
        messagebox.showerror("Error", "Username must start with a letter and contain no spaces!")
        return

    try:
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE username = ?", (username,))
        if c.fetchone():
            messagebox.showerror("Error", "Username already exists!")
            return
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {e}")
        return
    finally:
        conn.close()

    if not (contact.isdigit() and len(contact) == 10):
        messagebox.showerror("Error", "Contact must be a 10-digit number!")
        return
    
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        messagebox.showerror("Error", "Invalid email format!")
        return

    try:
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute("SELECT email FROM users WHERE email = ?", (email,))
        if c.fetchone():
            messagebox.showerror("Error", "Email already exists!")
            return
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {e}")
        return
    finally:
        conn.close()

    if len(password) < 6:
        messagebox.showerror("Error", "Passwords should be more than 6 characters.")
        return


    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return
    
    try:
        # Encrypt the password using Base64
        secret = password.encode('ascii')  # Encode the password to bytes
        secret = pybase64.b64encode(secret)  # Encrypt using Base64
        secret = secret.decode('ascii')  # Convert back to string for storage

        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute("""
            INSERT INTO users (fullname, email, username, contact, password)
            VALUES (?, ?, ?, ?, ?)
        """, (fullname, email, username, contact, secret))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        register.destroy()
        runpy.run_path(r'..\quizapp-tkinter\app\login.py')
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username or email already exists!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        conn.close()

def adjust_frames(event=None):
    register.update_idletasks()
    window_width = register.winfo_width()
    window_height = register.winfo_height()

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
    register_button.place(x=button_x, y=50)
    login_button.place(x=button_x + 100, y=50)

register.bind("<Configure>", adjust_frames)

framemain = Frame(register, bd=2, relief="ridge", padx=0, pady=0, bg=bgcolor)
framemain.place(x=0, y=0, width=700, height=400)

topframemain = Frame(register, bd=1, relief="ridge", padx=0, pady=0, bg=header_color)
topframemain.place(x=0, y=0, width=700, height=25)
Label(topframemain, text="Quiz App", font=("Arial", 12), padx=20, pady=0,fg='white',bg=header_color).place(x=0, y=0)

welcomeframe = Frame(register, bd=2, relief="ridge", padx=0, pady=0, bg=tablecolor)
welcomeframe.place(x=150, y=70, width=400, height=60)
Label(welcomeframe, text="Welcome to Quiz App", font=("Arial", 25, "bold"), bg=tablecolor,fg='white').pack(pady=10, padx=10)

maxminbtns(register)

frame = Frame(register, bd=2, relief="ridge", padx=20, pady=20, bg='white')
frame.place(x=100, y=140, width=500, height=250)

Label(frame, text="Name:", bg='white', fg='black').place(x=5, y=0)
name_entry = Entry(frame,bg='black',fg='white')
name_entry.place(x=5, y=20)

Label(frame, text="Username:", bg='white', fg='black').place(x=5, y=50)
user_entry = Entry(frame,bg='black',fg='white')
user_entry.place(x=5, y=70)

Label(frame, text="Contact Number:", bg='white', fg='black').place(x=5, y=100)
contact_entry = Entry(frame,bg='black',fg='white')
contact_entry.place(x=5, y=120)

Label(frame, text="E-mail:", bg='white', fg='black').place(x=5, y=150)
email_entry = Entry(frame,bg='black',fg='white')
email_entry.place(x=5, y=170)

Label(frame, text="Password:", bg='white', fg='black').place(x=250, y=0)
pass_entry = Entry(frame, show="*",bg='black',fg='white')
pass_entry.place(x=250, y=20)

Label(frame, text="Confirm Password:", bg='white', fg='black').place(x=250, y=50)
confirm_pass_entry = Entry(frame, show="*",bg='black',fg='white')
confirm_pass_entry.place(x=250, y=70)

Button(frame, text="Register", command=register_user,fg='white',bg=button_color).place(x=200, y=190)

infotopframe = Frame(register, bd=1, relief="ridge", padx=0, pady=0, bg=header_color)
infotopframe.place(x=100, y=140, width=500, height=20)
Label(infotopframe, text="Register", font=("Arial", 10), padx=15, pady=0, fg='white',bg=header_color).place(x=0, y=0)


backframe = Frame(register, bd=1, relief="ridge", padx=0, pady=0, bg='black')
backframe.place(x=450, y=140, width=50, height=20)

back_label = Label(backframe, text="Back", bg="black", fg="white", font=("Arial", 10))
back_label.place(x=0, y=0)
back_label.bind("<Button-1>", lambda e: back_to_welcome(register))

register_button = Button(framemain, text="Register", command=register_user, fg='white',bg=button_color)
register_button.place(x=500, y=30)

login_button = Button(framemain, text="Login", command=lambda: open_login(register), fg='white',bg=button_color)
login_button.place(x=600, y=30)

adjust_frames()
register.mainloop()
