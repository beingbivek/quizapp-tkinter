import sqlite3

def dbconnect(close):
    conn = sqlite3.connect('quiz.db')
    conn.commit()
    conn.close()
    return conn
