from tkinter import *
from tkinter import messagebox
import sqlite3
import runpy
import tkinter.font as font

# Colors (matched with Register page)
bgcolor = "#E0E0E0"
header_color = "#34495E"
frame_bg = "#E0E0E0"
button_color = '#1F618D'
tablecolor = '#34495E'
label_text_color = "black"  # Text color for labels

def back_to_welcome():
    user_login.destroy()
    runpy.run_path('welcome.py')

def open_login():
    user_login.destroy()
    runpy.run_path('login.py')

def open_registration():
    user_login.destroy()
    runpy.run_path('register.py')

def go_to_forgot():
    user_login.destroy()
    runpy.run_path('forgotps.py')

def open_admin_login():
    user_login.destroy()
    runpy.run_path('admin.py')

def login():
    username_or_email = name_entry.get().strip()
    password = user_entry.get().strip()

    if not username_or_email or not password:
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        # Connect to the database
        conn = sqlite3.connect('quiz.db')  # Replace with your actual database name
        c = conn.cursor()

        # Check if the username or email exists in the database
        c.execute("""
            SELECT * FROM users 
            WHERE username = ? OR email = ?
        """, (username_or_email, username_or_email))
        user = c.fetchone()

        if user:
            # Check if the password matches
            if user[6] == password:  # Assuming password is the 7th column in the table
                messagebox.showinfo("Success", "Login successful!")
                # Write user ID to a temporary file
                with open("temp_user_id.txt", "w") as f:
                    f.write(str(user[0]))  # Assuming user ID is the first column
                user_login.destroy()
                # Launch userdashboard.py in a new process
                OPEN_FILE = r'..\quizapp-tkinter\app\userdashboard.py'

                runpy.run_path(OPEN_FILE)
            else:
                messagebox.showerror("Error", "Incorrect password")
        else:
            messagebox.showerror("Error", "Username or email not found")

        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

user_login = Tk()
user_login.title("Login")
user_login.attributes('-fullscreen', True)

def adjust_frames(event=None):
    user_login.update_idletasks()
    window_width = user_login.winfo_width()
    window_height = user_login.winfo_height()
    x_main = (window_width - 700) // 2
    y_main = (window_height - 400) // 2
    button_x = window_width - 200
    
    framemain.place(x=0, y=0, width=window_width, height=window_height)
    topframemain.place(x=0, y=0, width=window_width, height=25)
    welcomeframe.place(x=x_main + 150, y=y_main + 70, width=400, height=60)
    frame.place(x=x_main + 200, y=y_main + 140, width=300, height=250)
    infotopframe.place(x=x_main + 200, y=y_main + 140, width=300, height=20)
    backframe.place(x=x_main + 450, y=y_main + 140, width=50, height=20)
    register_button.place(x=button_x, y=50)
    login_button.place(x=button_x + 100, y=50)

user_login.bind("<Configure>", adjust_frames)

framemain = Frame(user_login, bd=2, relief="ridge", padx=0, pady=0, bg=bgcolor)
framemain.place(x=0, y=0, width=700, height=400)

topframemain = Frame(user_login, bd=1, relief="ridge", padx=0, pady=0, bg=header_color)
topframemain.place(x=0, y=0, width=700, height=25)
Label(topframemain, text="Quiz App", font=("Arial", 12), padx=20, pady=0, bg=header_color, fg='white').place(x=0, y=0)

# Making close and minimize button manually
MAINFRAME_COLOR = "#E0E0E0"
SIDEBAR_COLOR = "#2C3E50"
BUTTON_COLOR = "#34495E"
HIGHLIGHT_COLOR = "#1A252F"
HEADER_COLOR = "#57a1f8"
PROFILE_COLOR = "#1F618D"
LOGOUT_COLOR = "#E74C3C"
FG_COLOR = "white"
button_font = font.Font(size=14)

def min():
    user_login.iconify()

def on_enter(i):
    btn2['background'] = "red"

def on_leave(i):
    btn2['background'] = HEADER_COLOR

def enter(i):
    btn['background'] = "red"

def leave(i):
    btn['background'] = HEADER_COLOR

def max():
    msg_box = messagebox.askquestion('Exit Application', 'Are you sure you want to close the application?', icon='warning')
    if msg_box == 'yes':
        user_login.destroy()

btn2 = Button(topframemain, text="✕", command=max, width=4, bg=HEADER_COLOR, border=1, font=button_font)
btn2.place(x=1125,y=-5)
btn2.bind('<Enter>', on_enter)
btn2.bind('<Leave>', on_leave)

btn = Button(topframemain, text="-", command=min, width=4, bg=HEADER_COLOR, border=1, font=button_font)
btn.place(x=1175,y=-5)
btn.bind('<Enter>', enter)
btn.bind('<Leave>', leave)

welcomeframe = Frame(user_login, bd=2, relief="ridge", padx=0, pady=0, bg=tablecolor)
welcomeframe.place(x=150, y=70, width=400, height=60)
Label(welcomeframe, text="Welcome to Quiz App", font=("Arial", 25, "bold"), bg=tablecolor, fg='white').pack(pady=10, padx=10)

frame = Frame(user_login, bd=2, relief="ridge", padx=20, pady=20, bg='white')
frame.place(x=200, y=140, width=300, height=250)

Label(frame, text="Email/Username:", bg='white', fg=label_text_color).place(x=5, y=0)
name_entry = Entry(frame, bg='black', fg='white')
name_entry.place(x=5, y=20)

Label(frame, text="Password:", bg='white', fg=label_text_color).place(x=5, y=50)
user_entry = Entry(frame, show="*", bg='black', fg='white')
user_entry.place(x=5, y=70)

Button(frame, text="Forgot Password", command=go_to_forgot, fg='white', bg=button_color).place(x=122, y=110)
Button(frame, text="Admin Login", command=open_admin_login, fg='white', bg=button_color).place(x=156, y=150)
Button(frame, text="Login", command=login, fg='white', bg=button_color).place(x=100, y=190)

infotopframe = Frame(user_login, bd=1, relief="ridge", padx=0, pady=0, bg=header_color)
infotopframe.place(x=200, y=140, width=300, height=20)
Label(infotopframe, text="Login", font=("Arial", 10), padx=15, pady=0, bg=header_color, fg='white').place(x=0, y=0)

backframe = Frame(user_login, bd=1, relief="ridge", padx=0, pady=0, bg='black')
backframe.place(x=450, y=140, width=50, height=20)

back_label = Label(backframe, text="Back", bg="black", fg="white", font=("Arial", 10))
back_label.place(x=0, y=0)
back_label.bind("<Button-1>", lambda e: back_to_welcome())

register_button = Button(framemain, text="Register", command=open_registration, fg='white', bg=button_color)
register_button.place(x=500, y=30)

login_button = Button(framemain, text="Login", command=open_login, fg='white', bg=button_color)
login_button.place(x=600, y=30)

adjust_frames()
user_login.mainloop()