import sys
import os

# Add the 'quizdb' folder to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'quizdb'))

# Now you can import 'database' from the 'quizdb' module
import database as db

import tkinter as tk

c = db.dbconnect(True)
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
db.dbconnect(False)
# print(db.dbconnect(False))

root = tk.Tk()
root.geometry('400x400')
root.title('Admin Dashboard')

e1 = Entry.

root.mainloop()