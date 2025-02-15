from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
from PIL import ImageTk, Image
import runpy
import sqlite3
from random import *
import pybase64
import re #For password validation.

# User window
root = Tk()
root.configure(bg="white")
root.attributes("-fullscreen", True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Importing defaults after root creation
from quizdefaults import *

root.title("Quiz App - User Dashboard")
root.configure(bg=MAINFRAME_COLOR)

# Edit profile Functions - mukesh
def submit():
    # password changed to base64 encrypt
    secret = validate_password.get()
    secret = secret.encode('ascii')
    secret = pybase64.b64encode(secret)
    secret = secret.decode('ascii')
    return secret
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

def update_profile_in_db(user_id, fullname, email, username, contact, address, password=None):
    """Update the user profile in the database."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        query = """
        UPDATE users
        SET fullname = ?, email = ?, username = ?, contact = ?, address = ?, password = ?
        WHERE user_id = ?
        """
        c.execute(query, (fullname, email, username, contact, address, submit(), user_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Profile updated successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def validate_password(password):
    """Validate the password to ensure it meets the requirements."""
    # Password must contain at least 1 uppercase letter, 1 lowercase letter, and 1 symbol
    if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[\W_]).+$', password,):
        return False
    return True

def update_profile():
    """Handle the update profile button click."""
    updated_values = [entry.get() for entry in entries]
    fullname, username, contact, email, address, new_password, confirm_password = updated_values

    # Check if the password fields are not empty
    if new_password or confirm_password:
        # If password fields are not empty, validate the password
        if new_password != confirm_password:
            messagebox.showerror("Error", "New password and confirm password do not match!")
            return

        if not validate_password(new_password):
            messagebox.showerror("Error", "Password must contain at least 1 uppercase letter, 1 lowercase letter, and 1 symbol!")
            return

        # Encrypt the password using base64
        password = new_password.encode('ascii')
        password = pybase64.b64encode(password).decode('ascii')
    else:
        # If password fields are empty, set password to None (do not update password)
        password = None

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
            password=password
        )

def cancel():
    """Close the application."""
    root.destroy()

# Load user profile data
users = load_profile()

# Making close and minimize button manually
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

label1 = LabelFrame(root, height=35, fg="blue", bg=HEADER_COLOR).place(x=0, y=0)
btn2 = Button(root, text="✕", command=max, width=4, bg=HEADER_COLOR, border=0, font=button_font)
btn2.pack(anchor="ne")
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

# Sidebar Frame
sidebar = Frame(root, bg=SIDEBAR_COLOR, width=200, height=600)
sidebar.pack(side='left', fill='y')

# Profile Image Placeholder
profile_img = Label(sidebar, text="Profile Image", bg='white', width=15, height=5)
profile_img.pack(pady=10)

# Username and Score
username_label = Label(sidebar, text="Aayush Bohara", fg=FG_COLOR, bg=SIDEBAR_COLOR, font=label_font)
username_label.pack()

score_label = Label(sidebar, text="Score: 1500", fg=FG_COLOR, bg=SIDEBAR_COLOR, font=("Arial", 10))
score_label.pack()

# Store button references
buttons = {}

# Submit Question of the day
def submitqotd():
    pass

# Sidebar Button Function
def openbutton(btn_text):
    # Clear the main content area
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    # Reset all button colors
    for btn in buttons.values():
        btn.configure(bg=BUTTON_COLOR)

    # Set the clicked button color
    buttons[btn_text].configure(bg=HIGHLIGHT_COLOR)

    # Main Dashboard Code
    if btn_text == "Dashboard":
        # Question of the Day
        qotd_label = Label(main_frame, text="Question of the day!", font=header_font, bg=MAINFRAME_COLOR)
        qotd_label.pack(anchor='w')

        topic_label = Label(main_frame, text="Topic: Loksewa/Animal", font=label_font, bg=MAINFRAME_COLOR)
        topic_label.pack(anchor='w')

        question_label = Label(main_frame, text="Q. How fast can a Cheetah run?", font=("Arial", 12), bg=MAINFRAME_COLOR)
        question_label.pack(anchor='w')

        options = ["80 kmph", "90 Kmph", "100 Kmph", "120 Kmph"]
        selected_option = StringVar()
        selected_option.set(None)

        for opt in options:
            Radiobutton(main_frame, text=opt, variable=selected_option, value=opt, bg=MAINFRAME_COLOR).pack(anchor='w')

        btn_submitqotd = Button(main_frame, text='Submit',bg=BUTTON_COLOR,command=submitqotd).pack(anchor='w')

        # Progress Table
        progress_label = Label(main_frame, text="Your Progress", font=("Arial", 14, "bold"), bg=MAINFRAME_COLOR)
        progress_label.pack(anchor='w', pady=10)

        columns = ("SN", "Courses", "Tackled", "Correct", "Incorrect")
        progress_table = ttk.Treeview(main_frame, columns=columns, show='headings', height=4)

        for col in columns:
            progress_table.heading(col, text=col)
            progress_table.column(col, width=100, anchor='center')

        progress_data = [(1, "CEE", 40, 30, 10), (2, "IOE", 38, 8, 30), (3, "Driving", 41, 1, 40), (4, "LokSewa", 45, 40, 5)]
        for row in progress_data:
            progress_table.insert('', END, values=row)
        progress_table.pack()

        # Mock Test Results Table
        mock_label = Label(main_frame, text="Previous Mock Test Results", font=("Arial", 14, "bold"), bg=MAINFRAME_COLOR)
        mock_label.pack(anchor='w', pady=10)

        mock_columns = ("SN", "Mock TestID", "Datetime", "Course", "Result")
        mock_table = ttk.Treeview(main_frame, columns=mock_columns, show='headings', height=4)

        for col in mock_columns:
            mock_table.heading(col, text=col)
            mock_table.column(col, width=120, anchor='center')

        mock_data = [(1, "CEE12", "2024/5/20 15:20", "CEE", "50/100"),
                     (2, "IOE312", "2024/5/20 15:20", "IOE", "50/100"),
                     (3, "Driving123", "2024/5/20 15:20", "Driving", "50/100"),
                     (4, "LokSewa4334", "2024/5/20 15:20", "Loksewa", "50/100")]

        for row in mock_data:
            mock_table.insert('', END, values=row)
        mock_table.pack()

    # Edit profile - user section - mukesh
    elif btn_text == "Profile":
        
        secframe = Frame(main_frame, bd=2, relief='ridge')
        secframe.place(x=50, y=50, width=900, height=700)

        username = Label(main_frame, text=users[3], font=('Arial', 14, 'bold')).place(x=462, y=255)

        canvas = Canvas(main_frame, width=200, height=200)
        canvas.place(x=420, y=55)
        canvas.create_oval(50, 50, 150, 150)


        # Labels and Entries
        labels_entries = [
            ("Name", 70, 320, users[1]),
            ("User Name", 70, 400, users[3]),
            ("Contact Number", 70, 480, users[4]),
            ("Email", 70, 560, users[2]),
            ("Address", 640, 480, users[5]),
            ("New Password", 640, 320, "",),
            ("Confirm Password", 640, 400, "")
        ]


        entries = []
        for text, x, y, value in labels_entries:
            Label(main_frame, text=text).place(x=x, y=y)
            if text in ["New Password", "Confirm Password"]:
                entry = Entry(main_frame, width=35, show="*")  # Mask the password fields
            else:
                entry = Entry(main_frame, width=35)
            entry.place(x=x, y=y+20)
            entry.insert(0, value)
            entries.append(entry)

        # Buttons
        Button(main_frame,text='UPDATE', bg="#34495E", fg="black", font=('Arial', 14, 'bold'), command=update_profile).place(x=screen_width/4.5, y=690)

        pass
    

    else:
        label = Label(main_frame, text=btn_text, font=("Arial", 20, "bold"), bg=MAINFRAME_COLOR)
        label.pack(expand=True)

# Sidebar Buttons
def sidebar_button(text, bg_color=BUTTON_COLOR):
    btn = Button(sidebar, text=text, bg=bg_color, fg=FG_COLOR, font=("Arial", 10, "bold"), width=20, height=2, bd=0, command=lambda: openbutton(text))
    btn.pack()
    buttons[text] = btn
    return btn

# Create and store buttons
sidebar_button("Dashboard", bg_color=HIGHLIGHT_COLOR)
sidebar_button("Courses")
sidebar_button("LeaderBoard")
sidebar_button("Mock Test")
sidebar_button("Profile")
sidebar_button("About US")

# Logout Button
logout_btn = Button(sidebar, text="Logout", bg=LOGOUT_COLOR, fg=FG_COLOR, font=("Arial", 10, "bold"), width=20, height=2, bd=0)
logout_btn.pack(side='bottom', pady=20)

# Main Content Frame
main_frame = Frame(root, bg=MAINFRAME_COLOR, padx=20, pady=20)
main_frame.pack(expand=True, fill='both')

# Initialize with Dashboard
openbutton("Dashboard")

root.mainloop()
