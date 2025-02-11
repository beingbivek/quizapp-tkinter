import sqlite3

def dbconnect(open):
    conn = sqlite3.connect('quiz.db')
    if open:
        return conn.cursor()
    else:
        conn.commit()
        # conn.close()
        return conn.close()
    # return conn
