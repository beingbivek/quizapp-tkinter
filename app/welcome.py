from tkinter import *
import sqlite3
from tkinter import messagebox
import tkinter.font as font

def create_database():
    try:
        # Database creation
        conn = sqlite3.connect(DATABASE_FILE)
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
            password TEXT NOT NULL,
            securityquestion TEXT NOT NULL,
            securityanswer TEXT NOT NULL
        )
        """)

        # Courses Table
        c.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            coursename TEXT NOT NULL,
            coursedesc TEXT
        )
        """)

        # Categories Table
        c.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL,
            course_id INTEGER NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
        """)

        # Mock Tests Table
        c.execute("""
        CREATE TABLE IF NOT EXISTS mocktests (
            mocktest_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mocktest_name TEXT NOT NULL,
            mocktest_desc TEXT,
            fullmark INTEGER NOT NULL,
            passmark INTEGER NOT NULL,
            fulltime INT NOT NULL
        )
        """)

        # Questions Table
        c.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            category_id INTEGER,
            question TEXT NOT NULL,
            correct_ans TEXT NOT NULL,
            incorrect_ans TEXT NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses(course_id),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
        """)

        # Mock Questions Table
        c.execute("""
        CREATE TABLE IF NOT EXISTS mockquestions (
            mockquestion_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mocktest_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            no_of_questions INTEGER NOT NULL,
            FOREIGN KEY (mocktest_id) REFERENCES mocktests(mocktest_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
        """)

        # Mock Test Results Table
        c.execute("""
        CREATE TABLE IF NOT EXISTS mocktestresults (
            result_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mocktest_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            result INTEGER NOT NULL,
            resulttime DATETIME,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id),
            FOREIGN KEY (mocktest_id) REFERENCES mocktests(mocktest_id)
        )
        """)

        # Commit database
        conn.commit()

    except sqlite3.Error as e:
        messagebox.showerror('Error Creating Database',f"An sqlite3 error occurred: {e}")

    except Exception as e:
        messagebox.showerror('Error Creating Database',f"An error occurred: {e}")

    finally:
        # Close the connection
        conn.close()

welcome = Tk()
welcome.title("Quiz App")
welcome.attributes('-fullscreen', True)

from quizdefaults import *

create_database()

# Function to center frames dynamically
def center_frames(event=None):
    welcome.update_idletasks()
    
    window_width = welcome.winfo_width()
    window_height = welcome.winfo_height()
    
    frame_width = 1000
    frame_height = 700
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

    x_message = (window_width - message_width - 100) // 2
    y_message = y_main + 140

    x_welcome = (window_width - welcome_width) // 2
    y_welcome = y_main + 70

    # Adjust frame positions
    framemain.place(x=0, y=0, width=window_width, height=window_height)
    topframemain.place(x=0, y=0, width=window_width, height=25)
    welcomeframe.place(x=x_welcome, y=y_welcome, width=400, height=60)
    frame.place(x=x_message, y=y_message, width=600, height=350)
    register_button.place(x=button_x, y=100)
    login_button.place(x=button_x + 100, y=100)

# Main frame
framemain = Frame(welcome, bd=2, relief="ridge", padx=0, pady=0, bg=bgcolor)
framemain.place(x=0, y=0, width=700, height=400)

# Top frame with title
topframemain = Frame(welcome, bd=1, relief="ridge", padx=0, pady=0, bg=header_color)
topframemain.place(x=0, y=0, width=700, height=25)
Label(topframemain, text="Quiz App", font=("Arial", 12), padx=20, pady=0, bg=header_color, fg="white").place(x=0, y=0)

# Making close and minimize button manually
maxminbtns(welcome)


# Welcome frame
welcomeframe = Frame(welcome, bd=2, relief="ridge", padx=0, pady=0, bg=tablecolor)
welcomeframe.place(x=150, y=70, width=400, height=60)
Label(welcomeframe, text="Welcome to Quiz App", font=("Arial", 25, "bold"), bg=tablecolor, fg="white").pack(pady=10, padx=10)

# Welcome message frame
frame = Frame(welcome, bd=2, relief="ridge", padx=20, pady=20, bg=frame_bg)
Label(frame, text=welcometxt, font=("Arial", 12), bg=frame_bg, fg=label_text_color).place(x=-10, y=0)

# Buttons
Button(frame, text="Register", command=lambda: open_registration(welcome), fg='white', bg=button_color, font=button_font).place(x=50, y=225)
Button(frame, text="Login", command=lambda: open_login(welcome), fg='white', bg=button_color, font= button_font).place(x=400, y=225)

# Top buttons
register_button = Button(framemain, text="Register", command=lambda: open_registration(welcome), fg='white', bg=button_color, font= button_font)
register_button.place(x=500, y=30)

login_button = Button(framemain, text="Login", command=lambda: open_login(welcome), fg='white', bg=button_color, font=button_font)
login_button.place(x=600, y=30)

# Bind the resize event to reposition elements dynamically
welcome.bind("<Configure>", center_frames)

# Call the function initially to center elements at startup
center_frames()

welcome.mainloop()