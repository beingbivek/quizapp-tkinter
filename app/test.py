import sqlite3
import json
from tkinter import Tk, Frame, Label, Button, StringVar, Radiobutton
from tkinter import ttk
from random import shuffle

# DATABASE_FILE = 'your_database.db'  # Replace with your actual database file

def get_courses():
    # Placeholder function to fetch courses
    return [
        (1, "Loksewa"),
        (2, "CEE"),
        (3, "IOE"),
        (4, "Driving")
    ]

def get_categories():
    # Placeholder function to fetch categories
    return [
        (1, "Category 1"),
        (2, "Category 2")
    ]

# Set logged-in user (Replace with actual login logic)
LOGGED_IN_USER_ID = 1  # Change this dynamically based on user session

def fetch_random_question():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT question_id, question, correct_ans, incorrect_ans, course_id, category_id FROM questions ORDER BY RANDOM() LIMIT 1")
    qotd_data = cursor.fetchone()
    
    conn.close()
    return qotd_data

def question_location(course_id, category_id):
    coursename = next((name[1] for name in get_courses() if course_id == name[0]), "Random")
    categoryname = next((name[1] for name in get_categories() if category_id == name[0]), "Question")
    return f"{coursename} {categoryname}"

def fetch_progress_data(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT c.course_id, c.coursename, COUNT(mr.result), 
               SUM(CASE WHEN mr.result >= 50 THEN 1 ELSE 0 END) AS correct,
               SUM(CASE WHEN mr.result < 50 THEN 1 ELSE 0 END) AS incorrect
        FROM mocktestresults mr
        JOIN courses c ON mr.course_id = c.course_id
        WHERE mr.user_id = ?
        GROUP BY c.course_id, c.coursename
    """, (user_id,))
    
    progress_data = cursor.fetchall()
    conn.close()
    return progress_data

def fetch_latest_mock_results(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT m.mocktest_id, m.mocktest_name, mr.result, c.coursename
        FROM mocktestresults mr
        JOIN mocktests m ON mr.mocktest_id = m.mocktest_id
        JOIN courses c ON mr.course_id = c.course_id
        WHERE mr.user_id = ?
        ORDER BY result_id DESC
        LIMIT 5
    """, (user_id,))
    
    mock_results = cursor.fetchall()
    conn.close()
    return mock_results

def create_table(frame, data):
    headers = ["SN", "Username", "Score"]
    for col, header in enumerate(headers):
        Label(frame, text=header, font=("Arial", 12, "bold"), bg="grey", width=10).grid(row=0, column=col, padx=1, pady=1)

    for row_idx, row_data in enumerate(data):
        for col_idx, value in enumerate(row_data):
            Label(frame, text=value, font=("Arial", 12), bg="white", width=10, relief="ridge").grid(row=row_idx + 1, column=col_idx, padx=1, pady=1)

root = Tk()
main_frame = Frame(root)
main_frame.pack()
from quizdefaults import *

header_font = ('Arial', 14, 'bold')
MAINFRAME_COLOR = "#FFFFFF"

header = Label(main_frame, text="Leaderboard", font=header_font, bg=MAINFRAME_COLOR)
header.pack(pady=10)

qotd_data = fetch_random_question()
question_id, question_text, correct_answer, incorrect_answers, course_id, category_id = qotd_data
incorrect_answers = json.loads(incorrect_answers)
options = incorrect_answers + [correct_answer]
shuffle(options)

qotd_label = Label(main_frame, text="Question of the Day!", font=("Arial", 16, "bold"), bg=MAINFRAME_COLOR)
qotd_label.pack(anchor='w')

topic_label = Label(main_frame, text=f"Topic: {question_location(course_id, category_id)}", font=("Arial", 12), bg=MAINFRAME_COLOR)
topic_label.pack(anchor='w')

question_label = Label(main_frame, text=f"Q. {question_text}", font=("Arial", 12), bg=MAINFRAME_COLOR)
question_label.pack(anchor='w')

selected_option = StringVar()
selected_option.set(None)

def check_answer():
    selected = selected_option.get()
    if selected == correct_answer:
        btn_submitqotd.config(state=DISABLED, text="Correct!", bg="green")
    else:
        btn_submitqotd.config(text="Try Again", bg="red")

for opt in options:
    rb = Radiobutton(main_frame, text=opt, variable=selected_option, value=opt, bg=MAINFRAME_COLOR)
    rb.pack(anchor='w')

btn_submitqotd = Button(main_frame, text='Submit', bg="grey", command=check_answer)
btn_submitqotd.pack(anchor='w')

# Progress Table
progress_label = Label(main_frame, text="Your Progress", font=("Arial", 14, "bold"), bg=MAINFRAME_COLOR)
progress_label.pack(anchor='w', pady=10)

columns = ("SN", "Courses", "Tackled", "Correct", "Incorrect")
progress_table = ttk.Treeview(main_frame, columns=columns, show='headings', height=4)

for col in columns:
    progress_table.heading(col, text=col)
    progress_table.column(col, width=100, anchor='center')

progress_data = fetch_progress_data(LOGGED_IN_USER_ID)
for i, row in enumerate(progress_data, start=1):
    progress_table.insert('', 'end', values=(i, *row))
progress_table.pack()

# Fetch Latest 5 Mock Test Results
mock_results = fetch_latest_mock_results(LOGGED_IN_USER_ID)

# Mock Test Results Table
mock_label = Label(main_frame, text="Previous Mock Test Results", font=("Arial", 14, "bold"), bg=MAINFRAME_COLOR)
mock_label.pack(anchor='w', pady=10)

mock_columns = ("SN", "Mock Test ID", "Datetime", "Course", "Result")
mock_table = ttk.Treeview(main_frame, columns=mock_columns, show='headings', height=4)

for col in mock_columns:
    mock_table.heading(col, text=col)
    mock_table.column(col, width=120, anchor='center')

for i, row in enumerate(mock_results, start=1):
    mock_table.insert('', 'end', values=(i, row[0], row[1], row[3], f"{row[2]}/100"))

mock_table.pack()

root.mainloop()

