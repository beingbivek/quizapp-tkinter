from tkinter import *
import runpy
import sqlite3
from tkinter import messagebox
import tkinter.font as font

def create_database():
    try:
        # Database creation
        conn = sqlite3.connect(QD.DATABASE_FILE)
        c = conn.cursor()

        # User table
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            contact TEXT,
            address TEXT,
            password TEXT NOT NULL
        )
        """)

        # Courses table
        c.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            coursename TEXT NOT NULL
        )
        """)

        # Courses-Categories table
        c.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name VARCHAR(100) NOT NULL,
            course_id INT,
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
        """)

        # Mocktest table
        c.execute("""
        CREATE TABLE IF NOT EXISTS mocktests (
            mocktest_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mocktest_name TEXT NOT NULL,
            fullmark INTEGER NOT NULL,
            passmark INTEGER NOT NULL
        )
        """)

        # Questions table
        c.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            category_id INTEGER,
            question TEXT NOT NULL,
            correct_ans TEXT NOT NULL,
            incorrect_ans TEXT NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses (course_id),
            FOREIGN KEY (category_id) REFERENCES categories (category_id)
        )
        ''')

        # Mockquestions table
        c.execute('''
        CREATE TABLE IF NOT EXISTS mockquestions (
            mockquestion_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mocktest_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            no_of_questions INTEGER NOT NULL,
            FOREIGN KEY (mocktest_id) REFERENCES mocktests (mocktest_id),
            FOREIGN KEY (course_id) REFERENCES courses (course_id),
            FOREIGN KEY (category_id) REFERENCES categories (category_id)
        )
        ''')

        # Mocktest results table
        c.execute('''
        CREATE TABLE IF NOT EXISTS mocktestresults (
            result_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mocktest_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            result INTEGER NOT NULL,
            resulttime DATETIME,
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (mocktest_id) REFERENCES mocktests (mocktest_id)
        )
        ''')

        # Commit database
        conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        conn.close()

# Colors (matched with Register page)
bgcolor = "#E0E0E0"  # Background color
header_color = "#34495E"  # Header color
frame_bg = "#E0E0E0"  # Frame background color
button_color = '#1F618D'  # Button color
tablecolor = '#34495E'  # Table color
label_text_color = "black"  # Text color for labels

welcome = Tk()
welcome.title("Quiz App")
welcome.attributes('-fullscreen', True)

import quizdefaults as QD

create_database()

def open_registration():
    welcome.destroy()
    runpy.run_path('register.py')

def open_login():
    welcome.destroy()
    runpy.run_path('login.py')

# Function to center frames dynamically
def center_frames(event=None):
    welcome.update_idletasks()
    
    window_width = welcome.winfo_width()
    window_height = welcome.winfo_height()
    
    frame_width = 700
    frame_height = 400
    message_width = 500
    message_height = 250
    welcome_width = 400
    welcome_height = 60

    if window_width > 700 or window_height > 400:
        x_main = (window_width - 700) // 2
        y_main = (window_height - 400) // 2
        button_x = window_width - 200
    else:
        x_main, y_main = 0, 0
        button_x = 500

    # Calculate center positions
    x_main = (window_width - frame_width) // 2
    y_main = (window_height - frame_height) // 2

    x_message = (window_width - message_width) // 2
    y_message = y_main + 140

    x_welcome = (window_width - welcome_width) // 2
    y_welcome = y_main + 70

    # Adjust frame positions
    framemain.place(x=0, y=0, width=window_width, height=window_height)
    topframemain.place(x=0, y=0, width=window_width, height=25)
    welcomeframe.place(x=x_welcome, y=y_welcome, width=400, height=60)
    frame.place(x=x_message, y=y_message, width=500, height=250)
    register_button.place(x=button_x, y=50)
    login_button.place(x=button_x + 100, y=50)

# Main frame
framemain = Frame(welcome, bd=2, relief="ridge", padx=0, pady=0, bg=bgcolor)
framemain.place(x=0, y=0, width=700, height=400)

# Top frame with title
topframemain = Frame(welcome, bd=1, relief="ridge", padx=0, pady=0, bg=header_color)
topframemain.place(x=0, y=0, width=700, height=25)
Label(topframemain, text="Quiz App", font=("Arial", 12), padx=20, pady=0, bg=header_color, fg="white").place(x=0, y=0)

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
    welcome.iconify()

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
        welcome.destroy()

btn2 = Button(topframemain, text="✕", command=max, width=4, bg=HEADER_COLOR, border=1, font=button_font)
btn2.place(x=1125,y=-5)
btn2.bind('<Enter>', on_enter)
btn2.bind('<Leave>', on_leave)

btn = Button(topframemain, text="-", command=min, width=4, bg=HEADER_COLOR, border=1, font=button_font)
btn.place(x=1175,y=-5)
btn.bind('<Enter>', enter)
btn.bind('<Leave>', leave)

# Welcome frame
welcomeframe = Frame(welcome, bd=2, relief="ridge", padx=0, pady=0, bg=tablecolor)
welcomeframe.place(x=150, y=70, width=400, height=60)
Label(welcomeframe, text="Welcome to Quiz App", font=("Arial", 25, "bold"), bg=tablecolor, fg="white").pack(pady=10, padx=10)

# Welcome message frame
frame = Frame(welcome, bd=2, relief="ridge", padx=20, pady=20, bg=frame_bg)
Label(frame, text='''
Get ready to explore a world of knowledge and sharpen your skills with ease. 
Our app offers a variety of tests and practice questions tailored for:

CEE (Common Entrance Exam)
Loksewa (Public Service Commission)
Driving License Preparation
IOE (Institute of Engineering)

Whether you're preparing for competitive exams or brushing up your knowledge,
Quiz App is here to help you succeed. Start your journey today!
''', font=("Arial", 13), bg=frame_bg, fg=label_text_color).place(x=-10, y=0)

# Buttons
Button(frame, text="Register", command=open_registration, fg='white', bg=button_color).place(x=0, y=190)
Button(frame, text="Login", command=open_login, fg='white', bg=button_color).place(x=390, y=190)

# Top buttons
register_button = Button(framemain, text="Register", command=open_registration, fg='white', bg=button_color)
register_button.place(x=500, y=30)

login_button = Button(framemain, text="Login", command=open_login, fg='white', bg=button_color)
login_button.place(x=600, y=30)

# Bind the resize event to reposition elements dynamically
welcome.bind("<Configure>", center_frames)

# Call the function initially to center elements at startup
center_frames()

welcome.mainloop()