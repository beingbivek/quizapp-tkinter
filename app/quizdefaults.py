from tkinter import *
from tkinter import messagebox
import tkinter.font as font
import runpy,pybase64

# Default colors for Dashboards
MAINFRAME_COLOR = "#E0E0E0"
SIDEBAR_COLOR = "#2C3E50"
BUTTON_COLOR = "#34495E"
HIGHLIGHT_COLOR = "#1A252F"
HEADER_COLOR = "#57a1f8"
PROFILE_COLOR = "#1F618D"
LOGOUT_COLOR = "#E74C3C"
FG_COLOR = "white"
accent_color = "#1F618D"

# Colors (Welcome, Login and Registration Page)
bgcolor = "#E0E0E0"  # Background color
header_color = "#34495E"  # Header color
frame_bg = "#E0E0E0"  # Frame background color
button_color = '#1F618D'  # Button color
tablecolor = '#34495E'  # Table color
label_text_color = "black"  # Text color for labels

# File path
DATABASE_FILE = r'..\quizapp-tkinter\quiz.db'
USER_FILE = r'..\quizapp-tkinter\\app\quizdb\user.txt'
ICON_FILE = r'..\quizapp-tkinter\app\images\icon\quizicon.ico'
ICON_FILE_WHITE = r'..\quizapp-tkinter\app\images\qa_white_icon.png'
ICON_FILE_BLACK = r'..\quizapp-tkinter\app\images\qa_black_icon.png'
ICON_FILE_WHITE_TOP = r'..\quizapp-tkinter\app\images\qa_white_icon_top.png'

# Font 
button_font = font.Font(size=14)
label_font = ("Arial", 12, "bold")
header_font = ("Arial", 16, "bold")
labelstyle = ("Helvatica", 14)

# encoding and decoding format
code = 'ascii'

# Encode and decode functions
def str_encode(value):
    secret = value.encode(code)  # Encode the password to bytes
    secret = pybase64.b64encode(secret)  # Encrypt using Base64
    secret = secret.decode(code)  # Convert back to string for storage
    return secret

def str_decode(value):
    secret = value.encode(code)  # Encode the password to bytes
    secret = pybase64.b64decode(secret)  # decode using Base64
    secret = secret.decode(code)  # Convert back to string which is the password
    return secret


# Defaults lists
defcourses = ['CEE','Driving','IOE','Loksewa']
security_questions = [
    "What was the name of your first pet?",
    "What is your mother's maiden name?",
    "What was the make and model of your first car?",
    "In what city were you born?",
    "What is the name of your favorite childhood teacher?",
    "What is your favorite book?",
    "What is your favorite movie?",
    "What is the name of your first school?",
    "What is your father's middle name?",
    "What was the name of your first childhood friend?",
    "What is your favorite food?",
    "What was your childhood nickname?",
    "What is the name of the street you grew up on?",
    "What was the name of your first employer?",
    "What was the first concert you attended?",
    "What is the name of your favorite sports team?",
    "What is your dream job?",
    "What was the name of your first stuffed animal?",
    "Where did you go on your first vacation?",
    "What is the name of your favorite musician or band?"
]
incorrect = ['China','Japan','Mexico']
dummyquestion = [1,'Where is the highest peak in the world?','Nepal',incorrect,1,1]


# Paths for runpy
def open_registration(root):
    root.destroy()
    runpy.run_path(r'..\quizapp-tkinter\app\register.py')

def open_login(root):
    root.destroy()
    runpy.run_path(r'..\quizapp-tkinter\app\login.py')

def back_to_welcome(root):
    root.destroy()
    runpy.run_path(r'..\quizapp-tkinter\app\welcome.py')

def go_to_forgot(root):
    root.destroy()
    runpy.run_path(r'..\quizapp-tkinter\app\forgotps.py')

def open_admin_login(root):
    root.destroy()
    runpy.run_path(r'..\quizapp-tkinter\app\admin.py')

def open_user_dashboard(root):
    root.destroy()
    runpy.run_path(r'..\quizapp-tkinter\app\userdashboard.py')

def open_admin_dashboard(root):
    root.destroy()
    runpy.run_path(r'..\quizapp-tkinter\app\admindashboard.py')


# Welcome text
welcometxt = '''
Get ready to explore a world of knowledge and sharpen your skills with ease. 
Our app offers a variety of tests and practice questions tailored for:

CEE (Common Entrance Exam)
Loksewa (Public Service Commission)
Driving License Preparation
IOE (Institute of Engineering)
And More..

Whether you're preparing for competitive exams or brushing up your knowledge,
Quiz App is here to help you succeed. Start your journey today!
'''

# Max Min Buttons
def minclose_windowbtn(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    def min():
        root.iconify()

    def on_enter(i):
        btn2['background'] = "red"

    def on_leave(i):
        btn2['background'] = HEADER_COLOR

    def max():
        msg_box = messagebox.askquestion('Exit Application', 'Are you sure you want to close the application?', icon='warning')
        if msg_box == 'yes':
            root.destroy()

    Label(root, text="Quiz App", font=("Arial", 12), padx=20, pady=5, bg=header_color, fg='white',width=screen_width).place(x=0, y=0)

    label1 = LabelFrame(root, height=35, fg="blue", bg=HEADER_COLOR).place(x=0, y=0)
    btn2 = Button(root, text="✕", command=max, width=4, bg=HEADER_COLOR, border=0, font=button_font)
    btn2.pack(anchor="ne")

    # Hover Functinality
    btn2.bind('<Enter>', on_enter)
    btn2.bind('<Leave>', on_leave)

    btn = Button(root, text="-", command=min, width=4, bg=HEADER_COLOR, border=0, font=button_font)
    btn.place(x=screen_width-100, y=0)

    def enter(i):
        btn['background'] = "red"

    def leave(i):
        btn['background'] = HEADER_COLOR

    btn.bind('<Enter>', enter)
    btn.bind('<Leave>', leave)

def delete_data(conn, table_name, primary_key_column, primary_key_value):
    """
    Deletes data from a table and its associated data in related tables.
    
    Parameters:
        conn: SQLite database connection object.
        table_name: Name of the table from which to delete data.
        primary_key_column: Name of the primary key column in the table.
        primary_key_value: Value of the primary key for the record to delete.
    """
    try:
        cursor = conn.cursor()

        # Define the order of deletion based on table relationships
        deletion_order = [
            "mocktestresults",  # Child of mocktests, users, and courses
            "mockquestions",     # Child of mocktests, courses, and categories
            "questions",         # Child of courses and categories
            "categories",        # Child of courses
            "mocktests",         # Parent of mockquestions and mocktestresults
            "courses",           # Parent of categories, questions, mockquestions, and mocktestresults
            "users"              # Parent of mocktestresults
        ]

        # Check if the table is in the deletion order
        if table_name not in deletion_order:
            raise ValueError(f"Table '{table_name}' is not supported for deletion.")

        # Get the index of the table in the deletion order
        table_index = deletion_order.index(table_name)

        # Delete data from the specified table and its child tables
        for table in deletion_order[table_index:]:
            if table == table_name:
                # Delete from the specified table
                query = f"DELETE FROM {table_name} WHERE {primary_key_column} = ?"
            else:
                # Delete from child tables
                if table == "mocktestresults":
                    query = f"DELETE FROM mocktestresults WHERE {primary_key_column} = ?"
                elif table == "mockquestions":
                    query = f"DELETE FROM mockquestions WHERE {primary_key_column} = ?"
                elif table == "questions":
                    query = f"DELETE FROM questions WHERE {primary_key_column} = ?"
                elif table == "categories":
                    query = f"DELETE FROM categories WHERE {primary_key_column} = ?"
                elif table == "mocktests":
                    query = f"DELETE FROM mocktests WHERE {primary_key_column} = ?"
                elif table == "courses":
                    query = f"DELETE FROM courses WHERE {primary_key_column} = ?"
                elif table == "users":
                    query = f"DELETE FROM users WHERE {primary_key_column} = ?"

            cursor.execute(query, (primary_key_value,))
            print(f"Deleted from {table}: {cursor.rowcount} rows affected.")

        # Commit the changes
        conn.commit()
        print("Deletion completed successfully.")

    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"Error during deletion: {e}")
    finally:
        # Close the cursor
        cursor.close()
