from tkinter import *
from tkinter import messagebox
import sqlite3
import re  # For password validation using regular expressions
import pybase64

# Database file path
DATABASE_FILE = r'C:\Project\quizapp-tkinter\quiz.db'

def submit():
    # password changed to base64 encrypt
    secret = validate_password.get()
    secret = secret.encode('ascii')
    secret = pybase64.b64encode(secret)
    secret = secret.decode('ascii')
    
    # To decrypt
    '''
    secret = password.get() # put the password variable
    secret = secret.encode('ascii')
    secret = pybase64.b64decode(secret)
    secret = secret.decode('ascii') # this is the final password
    '''
    
def load_profile():
    """Load user profile data from the database."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute('SELECT * FROM users')
        users = c.fetchall()
        conn.close()
        return users[0]  # Return the first user's data (assuming there's only one user for simplicity)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return ['Mukesh Babu Acharya', 'babu@gmail.com', 'Babu.net', '9862148844', '123 Main Street', 'password']

def update_profile_in_db(user_id, fullname, email, username, contact, address, password):
    """Update the user profile in the database."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        query = """
        UPDATE users
        SET fullname = ?, email = ?, username = ?, contact = ?, address = ?, password = ?
        WHERE user_id = ?
        """
        c.execute(query, (fullname, email, username, contact, address, password, user_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Profile updated successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def validate_password(password):
    """Validate the password to ensure it meets the requirements."""
    # Password must contain at least 1 uppercase letter, 1 lowercase letter, and 1 symbol
    if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[\W_]).+$', password):
        return False
    return True

def update_profile():
    """Handle the update profile button click."""
    updated_values = [entry.get() for entry in entries]
    fullname, username, contact, email, address, new_password, confirm_password = updated_values

    # Check if the new password and confirm password match
    if new_password != confirm_password:
        messagebox.showerror("Error", "New password and confirm password do not match!")
        return

    # Validate the password
    if not validate_password(new_password):
        messagebox.showerror("Error", "Password must contain at least 1 uppercase letter, 1 lowercase letter, and 1 symbol!")
        return

    # Ask for confirmation
    confirm = messagebox.askyesno("Confirm Update", "Are you sure you want to update your profile?")
    if confirm:
        # Update the profile in the database
        update_profile_in_db(
            user_id=users[0],  # Assuming the first column is user_id
            fullname=fullname,
            email=email,
            username=username,
            contact=contact,
            address=address,
            password=new_password
        )

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

username = Label(root, text=users[3], font=('Arial', 14, 'bold')).place(x=445, y=255)

canvas = Canvas(root, width=200, height=200)
canvas.place(x=420, y=55)
canvas.create_oval(50, 50, 150, 150)

# Labels and Entries
labels_entries = [
    ("Name", 70, 320, users[1]),
    ("User Name", 70, 400, users[3]),
    ("Contact Number", 70, 480, users[4]),
    ("Email", 70, 560, users[2]),
    ("Address", 640, 480, users[5]),
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