import sqlite3
from tkinter import *
root = Tk()
from quizdefaults import *
import sqlite3
import random
import pybase64
import json  # To store incorrect answers as a JSON list
from datetime import datetime

# DATABASE_FILE = "your_database.db"  # Replace with your actual database path

# Connect to the database
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()
# User table
cursor.execute("""
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
print('table made')

# Courses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    coursename TEXT NOT NULL,
    coursedesc TEXT
)
""")
print('table made')

# Courses-Categories table
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(100) NOT NULL,
    course_id INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
)
""")
print('table made')

# Mocktest table
cursor.execute("""
CREATE TABLE IF NOT EXISTS mocktests (
    mocktest_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mocktest_name TEXT NOT NULL,
    mocktest_desc TEXT,
    fullmark INTEGER NOT NULL,
    passmark INTEGER NOT NULL
)
""")
print('table made')

# Questions table
cursor.execute('''
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
print('table made')

# Mockquestions table
cursor.execute('''
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
print('table made')

# Leaderboard table
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS leaderboard (
#     lb_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_id INTEGER NOT NULL,
#     course_id INTEGER NOT NULL,
#     score INTEGER NOT NULL,
#     scoredtime DATETIME,
#     FOREIGN KEY (user_id) REFERENCES users (user_id),
#     FOREIGN KEY (course_id) REFERENCES courses (course_id)
# )
# ''')

# Mocktest results table
cursor.execute('''
CREATE TABLE IF NOT EXISTS mocktestresults (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mocktest_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    result INTEGER NOT NULL,
    resulttime DATETIME,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (course_id) REFERENCES courses (course_id),
    FOREIGN KEY (mocktest_id) REFERENCES mocktests (mocktest_id)
)
''')
print('table made')

# Commit database
conn.commit()

### Insert 30 Dummy Users
users_data = [
    (f"User{i}", f"user{i}@example.com", f"user{i}", f"98000000{i}", f"City{i}", f"{pybase64.b64encode('password{i}'.encode('ascii'))}")
    for i in range(1, 31)
]
cursor.executemany(
    "INSERT INTO users (fullname, email, username, contact, address, password) VALUES (?, ?, ?, ?, ?, ?)", 
    users_data
)

### Insert 5 Courses
courses_data = [
    ("Loksewa", "Government Job Preparation"),
    ("CEE", "Common Entrance Exam"),
    ("IOE", "Institute of Engineering Exam"),
    ("Driving", "Driving License Test"),
    ("Medical", "Medical Entrance Exam"),
]
cursor.executemany(
    "INSERT INTO courses (coursename, coursedesc) VALUES (?, ?)", 
    courses_data
)

### Insert 20 Categories (Each course gets 4 categories)
categories_data = [
    (f"Category {i}", random.randint(1, 5))  # Assign random course_id (1 to 5)
    for i in range(1, 21)
]
cursor.executemany(
    "INSERT INTO categories (category_name, course_id) VALUES (?, ?)", 
    categories_data
)

### Insert 5 Mock Tests
mocktests_data = [
    ("Loksewa Test", "Loksewa Preparation Test", 100, 50),
    ("CEE Test", "CEE Preparation Test", 100, 50),
    ("IOE Test", "IOE Preparation Test", 100, 50),
    ("Driving Test", "Driving License Preparation", 100, 50),
    ("Medical Test", "Medical Entrance Test", 100, 50),
]
cursor.executemany(
    "INSERT INTO mocktests (mocktest_name, mocktest_desc, fullmark, passmark) VALUES (?, ?, ?, ?)", 
    mocktests_data
)

### Insert 20 Mock Questions (Each mock test gets 4 mock questions)
mockquestions_data = [
    (
        random.randint(1, 5),  # Random mock test ID (1 to 5)
        random.randint(1, 5),  # Random course ID (1 to 5)
        random.randint(1, 20), # Random category ID (1 to 20)
        random.randint(5, 20)  # Random number of questions (5 to 20)
    )
    for _ in range(20)
]
cursor.executemany(
    "INSERT INTO mockquestions (mocktest_id, course_id, category_id, no_of_questions) VALUES (?, ?, ?, ?)", 
    mockquestions_data
)

### Insert 50 Questions
questions_data = [
    (
        random.randint(1, 5),  # Random course ID (1 to 5)
        random.randint(1, 20), # Random category ID (1 to 20)
        f"Sample Question {i}?",  # Question text
        f"Correct Answer {i}",  # Correct answer
        json.dumps([f"Wrong {i}A", f"Wrong {i}B", f"Wrong {i}C"])  # Incorrect answers in list format
    )
    for i in range(1, 51)
]
cursor.executemany(
    "INSERT INTO questions (course_id, category_id, question, correct_ans, incorrect_ans) VALUES (?, ?, ?, ?, ?)", 
    questions_data
)

### Insert 40 Mock Test Results (Random users taking random courses)
mocktestresults_data = [
    (
        random.randint(1, 5),  # Random mock test ID
        random.randint(1, 30), # Random user ID (1 to 30)
        random.randint(1, 5),  # Random course ID (1 to 5)
        random.randint(50, 100),  # Random score (between 50 and 100)
        datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Date time of now
    )
    for _ in range(40)
]
cursor.executemany(
    "INSERT INTO mocktestresults (mocktest_id, user_id, course_id, result,resulttime) VALUES (?, ?, ?, ?, ?)", 
    mocktestresults_data
)

# Commit and close connection
conn.commit()
conn.close()

print("Dummy data inserted successfully!")
