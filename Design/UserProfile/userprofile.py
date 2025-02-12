from tkinter import *
from tkinter import messagebox
import sqlite3

# File to store user profile data
PROFILE_FILE = "user_profile.txt"

def load_profile():
    """Load user profile data from a text file."""
    try:
        conn = sqlite3.connect('C:\Project\quizapp-tkinter\quiz.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users')
        users = c.fetchall()
        print(users[0][1])
        conn.close()
        return users
        # with open(PROFILE_FILE, "r") as file:
        #     # Read all lines from the file and strip newline characters
        #     return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        # Return default data if the file doesn't exist
        return ['Mukesh Babu Acharya', 'Babu.net', '9862148844', 'babu@gmail.com']

def save_profile(data):
    """Save user profile data to a text file."""
    with open(PROFILE_FILE, "w") as file:
        # Write each field to a new line in the file
        for item in data:
            file.write(item + "\n")

def update_profile():
    """Update the user profile and save it to the file."""
    updated_values = [entry.get() for entry in entries]
    users[:] = updated_values[:4]  # Only update the first four fields
    save_profile(users)
    messagebox.showinfo("Profile Updated", "Your profile has been updated successfully!")

def cancel():
    """Close the application."""
    root.destroy()

# Load user profile data
users = load_profile()

# Initialize the Tkinter application
root = Tk()
root.title("User Profile")
root.geometry("1000x800")

# Frames
mainframe = Frame(root, bd=2, relief="ridge")
mainframe.place(x=0, y=0, width=1000, height=800)

secframe = Frame(root, bd=2, relief='ridge')
secframe.place(x=50, y=50, width=900, height=700)

username = Label(root, text=users[0][3], font=('Arial', 14, 'bold')).place(x=445, y=255)

canvas = Canvas(root, width=200, height=200)
canvas.place(x=420, y=55)
canvas.create_oval(50, 50, 150, 150)

# Labels and Entries
labels_entries = [
    ("Name", 70, 320, users[0][1]),
    ("User Name", 70, 400, users[0][3]),
    ("Contact Number", 70, 480, users[0][4]),
    ("Email", 70, 560, users[0][2]),
    ("Address", 640, 480, users[0][5]),
    ("New Password", 640, 320, ""),
    ("Confirm Password", 640, 400, "")
]

entries = []
for text, x, y, value in labels_entries:
    Label(root, text=text).place(x=x, y=y)
    entry = Entry(root, width=35)
    entry.place(x=x, y=y+20)
    entry.insert(0, value)
    entries.append(entry)

# Buttons
Button(text='UPDATE', bg="#34495E", fg="black", font=('Arial', 14, 'bold'), command=update_profile).place(x=83, y=690)
Button(text='CANCEL', bg="#E74C3C", fg="black", font=('Arial', 14, 'bold'), command=cancel).place(x=800, y=690)

root.mainloop()