import sqlite3
import pybase64
import json
from faker import Faker
from datetime import datetime, timedelta
import random
from tkinter import *
from tkinter import messagebox

root = Tk()
from quizdefaults import *
root.destroy()

# Default values (replace with your actual defaults)
# DATABASE_FILE = "quiz.db"
# security_questions = [
#     "What is your mother's maiden name?",
#     "What was the name of your first pet?",
#     "What city were you born in?"
# ]

def create_database():
    try:
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
            password TEXT NOT NULL,
            securityquestion TEXT NOT NULL,
            securityanswer TEXT NOT NULL,
            timestamp DATETIME NOT NULL
        )""")

        # Courses Table
        c.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            coursename TEXT NOT NULL,
            coursedesc TEXT
        )""")

        # Categories Table
        c.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL,
            course_id INTEGER NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )""")

        # Mock Tests Table
        c.execute("""
        CREATE TABLE IF NOT EXISTS mocktests (
            mocktest_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mocktest_name TEXT NOT NULL,
            mocktest_desc TEXT,
            fullmark INTEGER NOT NULL,
            passmark INTEGER NOT NULL,
            fulltime INT NOT NULL
        )""")

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
        )""")

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
        )""")

        # Mock Test Results Table
        c.execute("""
        CREATE TABLE IF NOT EXISTS mocktestresults (
            result_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mocktest_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            result INTEGER NOT NULL,
            resulttime DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id),
            FOREIGN KEY (mocktest_id) REFERENCES mocktests(mocktest_id)
        )""")

        conn.commit()
    except Exception as e:
        messagebox.showerror('Database Error', f"Error creating database: {str(e)}")
    finally:
        conn.close()

# Custom datetime formatting without 'T'
def adapt_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def convert_datetime(text):
    value = text.decode()
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("datetime", convert_datetime)

fake = Faker()

def encode_data(data):
    return pybase64.b64encode(data.encode('ascii')).decode('ascii')

def create_connection():
    return sqlite3.connect(DATABASE_FILE, detect_types=sqlite3.PARSE_DECLTYPES)

def generate_users(conn, count=50):
    c = conn.cursor()
    for _ in range(count):
        timestamp = fake.date_time_between(start_date='-3months', end_date='now').replace(microsecond=0)
        user = (
            fake.name(),
            fake.unique.email(),
            fake.user_name(),
            fake.phone_number(),
            encode_data("Password123!"),
            random.choice(security_questions),
            encode_data(fake.word()),
            timestamp
        )
        c.execute('''INSERT INTO users (fullname, email, username, contact,
                  password, securityquestion, securityanswer, timestamp)
                  VALUES (?,?,?,?,?,?,?,?)''', user)
    conn.commit()

def generate_courses(conn):
    courses = [
        ("Medical Entrance Exam", "NEET preparation course covering Physics, Chemistry, Biology"),
        ("Engineering Entrance Exam", "JEE Main preparation with Physics, Math, Chemistry"),
        ("Grade 11 Entrance", "School level entrance exam for science stream"),
        ("Driving License Exam", "Theoretical driving knowledge test"),
        ("Loksewa Exam", "Public service commission exam preparation")
    ]
    conn.executemany('INSERT INTO courses (coursename, coursedesc) VALUES (?,?)', courses)
    conn.commit()

def generate_categories(conn):
    categories = [
        ("Human Anatomy", 1), ("Biochemistry", 1), ("Pharmacology", 1), ("Pathology", 1),
        ("Physics", 2), ("Mathematics", 2), ("Chemistry", 2), ("Aptitude", 2),
        ("Basic Math", 3), ("General Science", 3), ("English", 3), ("Logical Reasoning", 3),
        ("Traffic Signs", 4), ("Vehicle Maintenance", 4), ("Road Ethics", 4), ("Driving Laws", 4)
    ]
    conn.executemany('INSERT INTO categories (category_name, course_id) VALUES (?,?)', categories)
    conn.commit()

def generate_questions(conn):
    c = conn.cursor()
    questions_data = [
        ("What is the SI unit of force?", "Newton", ["Joule", "Watt", "Pascal"]),
        ("Which law states F = ma?", "Newton's Second Law", ["Ohm's Law", "Boyle's Law", "Hooke's Law"]),
        ("What is the value of π (pi) to two decimal places?", "3.14", ["2.71", "1.61", "4.66"]),
        ("Solve for x: 2x + 5 = 15", "5", ["7", "10", "3"]),
        ("What does a red triangle sign indicate?", "Warning", ["Mandatory", "Prohibition", "Information"]),
        ("Blue circular sign typically indicates:", "Mandatory instruction", ["Warning", "Prohibition", "Tourist info"])
    ]
    
    for category_id in range(1, 17):
        for _ in range(10):
            question, correct, incorrect = random.choice(questions_data)
            c.execute('''INSERT INTO questions (course_id, category_id, question,
                      correct_ans, incorrect_ans) VALUES (?,?,?,?,?)''',
                      ((category_id-1)//4 +1, category_id, question, correct, json.dumps(incorrect)))
    conn.commit()

def generate_mocktests(conn):
    mocktests = [
        ("NEET Mock Test 1", "Full syllabus practice test", 100, 40, 120),
        ("JEE Main Mock Test", "Engineering entrance practice", 100, 40, 120),
        ("Class 11 Entrance Practice", "School level test", 50, 20, 60),
        ("Driving Theory Test", "DVSA style questions", 50, 35, 90)
    ]
    conn.executemany('''INSERT INTO mocktests (mocktest_name, mocktest_desc, fullmark,
                     passmark, fulltime) VALUES (?,?,?,?,?)''', mocktests)
    conn.commit()

def generate_mocktest_results(conn):
    c = conn.cursor()
    for user_id in range(1, 51):
        for mocktest_id in range(1, 5):
            result = random.randint(40, 100)
            result_time = fake.date_time_between(start_date='-3months', end_date='now').replace(microsecond=0)
            c.execute('''INSERT INTO mocktestresults (mocktest_id, user_id, course_id,
                      result, resulttime) VALUES (?,?,?,?,?)''',
                      (mocktest_id, user_id, mocktest_id, result, result_time))
    conn.commit()

def main():
    conn = create_connection()
    try:
        generate_users(conn)
        generate_courses(conn)
        generate_categories(conn)
        generate_questions(conn)
        generate_mocktests(conn)
        generate_mocktest_results(conn)
    except Exception as e:
        messagebox.showerror('Data Generation Error', f"Error generating data: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_database()
    main()
    root.mainloop()