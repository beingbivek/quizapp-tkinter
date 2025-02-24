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
    securityquestion TEXT NOT NULL,
    securityanswer TEXT NOT NULL
)
""")

# Courses Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    coursename TEXT NOT NULL,
    coursedesc TEXT
)
""")

# Categories Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL,
    course_id INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
)
""")

# Mock Tests Table
cursor.execute("""
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
cursor.execute("""
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
cursor.execute("""
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
cursor.execute("""
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

# Commit schema changes
conn.commit()

### Insert predefined Courses and Categories ###
courses = [
    ("Loksewa", "Government Job Preparation"),
    ("CEE", "Common Entrance Exam"),
    ("IOE", "Institute of Engineering Exam"),
    ("Medical", "Medical Entrance Exam"),
]
cursor.executemany("INSERT INTO courses (coursename, coursedesc) VALUES (?, ?)", courses)

# Fetch assigned Course IDs
cursor.execute("SELECT course_id FROM courses")
course_ids = [row[0] for row in cursor.fetchall()]

# Assign Categories
categories = []
for course_id in course_ids:
    for i in range(1, 5):
        categories.append((f"Category {i} for Course {course_id}", course_id))
cursor.executemany("INSERT INTO categories (category_name, course_id) VALUES (?, ?)", categories)

# Fetch assigned Category IDs
cursor.execute("SELECT category_id, course_id FROM categories")
category_course_map = cursor.fetchall()

# Insert Questions (10 per Category)
questions = []
for category_id, course_id in category_course_map:
    for i in range(1, 11):
        questions.append(
            (course_id, category_id, f"Sample Question {i} for Category {category_id}?", f"Correct {i}", json.dumps([f"Wrong {i}A", f"Wrong {i}B", f"Wrong {i}C"]))
        )
cursor.executemany("INSERT INTO questions (course_id, category_id, question, correct_ans, incorrect_ans) VALUES (?, ?, ?, ?, ?)", questions)

# Insert Mock Tests
mocktests = [
    ("Loksewa Test", "Loksewa Preparation Test", 100, 50, 1),
    ("CEE Test", "CEE Preparation Test", 100, 50, 2),
    ("IOE Test", "IOE Preparation Test", 100, 50, 3),
    ("Medical Test", "Medical Entrance Test", 100, 50, 4),
]
cursor.executemany("INSERT INTO mocktests (mocktest_name, mocktest_desc, fullmark, passmark, fulltime) VALUES (?, ?, ?, ?, ?)", mocktests)

# Fetch assigned Mock Test IDs
cursor.execute("SELECT mocktest_id FROM mocktests")
mocktest_ids = [row[0] for row in cursor.fetchall()]

# Assign Mock Questions (10 per Category for Each Mock Test)
mockquestions = []
for mocktest_id in mocktest_ids:
    for category_id, course_id in category_course_map:
        mockquestions.append((mocktest_id, course_id, category_id, random.randint(1,10)))
cursor.executemany("INSERT INTO mockquestions (mocktest_id, course_id, category_id, no_of_questions) VALUES (?, ?, ?, ?)", mockquestions)

# Commit and close connection
conn.commit()
conn.close()

print("Database setup and structured data insertion complete!")
