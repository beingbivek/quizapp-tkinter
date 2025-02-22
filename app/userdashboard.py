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

# Functions
# How many courses
def get_courses():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM courses')
    courses = c.fetchall()
    conn.close()
    return courses

def get_categories(course_id=None):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    if course_id:
        cursor.execute("SELECT * FROM categories WHERE course_id = ?", (course_id,))
    else:
        cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    categories = [list(category) for category in categories]
    # print(categories)
    courses = get_courses()
    # print(courses)

    for category in categories:
        for course in courses:
            if category[2] == course[0]:
                category[2] = course[1]
                break
    conn.close()
    return categories

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
        # Set logged-in user (Replace with actual login logic)
        LOGGED_IN_USER_ID = 1  # Change this dynamically based on user session

        # Connect to database
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # Fetch Random Question for "Question of the Day"
        cursor.execute("SELECT question_id, question, correct_ans, incorrect_ans, course_id, category_id FROM questions ORDER BY RANDOM() LIMIT 1")
        qotd_data = cursor.fetchone()
        question_id, question_text, correct_answer, incorrect_answers, course_id, category_id = qotd_data

        # Parse incorrect answers stored as JSON list
        import json
        incorrect_answers = json.loads(incorrect_answers)
        options = incorrect_answers + [correct_answer]
        shuffle(options)

        def question_location():
            coursename = next((name[1] for name in get_courses() if course_id == name[0]),"Random")
            categoryname = next((name[1] for name in get_categories() if category_id == name[0]),"Question")
            return coursename + ' ' + categoryname

        conn.close()  # Close database connection after fetching question

        # Question of the Day
        qotd_label = Label(main_frame, text="Question of the Day!", font=("Arial", 16, "bold"), bg=MAINFRAME_COLOR)
        qotd_label.pack(anchor='w')

        topic_label = Label(main_frame, text=f"Topic: {question_location()}", font=("Arial", 12), bg=MAINFRAME_COLOR)
        topic_label.pack(anchor='w')

        question_label = Label(main_frame, text=f"Q. {question_text}", font=("Arial", 12), bg=MAINFRAME_COLOR)
        question_label.pack(anchor='w')

        selected_option = StringVar()
        selected_option.set(None)

        option_buttons = []
        def check_answer():
            selected = selected_option.get()
            if selected == correct_answer:
                btn_submitqotd.config(state=DISABLED, text="Correct!", bg="green")
            else:
                btn_submitqotd.config(text="Try Again", bg="red")

        for opt in options:
            rb = Radiobutton(main_frame, text=opt, variable=selected_option, value=opt, bg=MAINFRAME_COLOR)
            rb.pack(anchor='w')
            option_buttons.append(rb)

        btn_submitqotd = Button(main_frame, text='Submit', bg=BUTTON_COLOR, command=check_answer)
        btn_submitqotd.pack(anchor='w')

        # Progress table Function
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
                    """, (LOGGED_IN_USER_ID,))


        mock_results = cursor.fetchall()
        conn.close()

        # Mock Test Results Table
        mock_label = Label(main_frame, text="Previous Mock Test Results", font=("Arial", 14, "bold"), bg=MAINFRAME_COLOR)
        mock_label.pack(anchor='w', pady=10)

        mock_columns = ("SN", "Mock Test ID", "Datetime", "Course", "Result")
        mock_table = ttk.Treeview(main_frame, columns=mock_columns, show='headings', height=4)

        for col in mock_columns:
            mock_table.heading(col, text=col)
            mock_table.column(col, width=120, anchor='center')

        for i, row in enumerate(mock_results, start=1):
            mock_table.insert('', END, values=(i, row[0], row[1], row[3], f"{row[2]}/100"))

        mock_table.pack()

        
    #Leaderboard user section.    
    elif btn_text == "LeaderBoard":

        LOGGED_IN_USER = "user10"  # Change this dynamically based on the logged-in user

        def fetch_leaderboard_data(logged_in_user):
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    c.coursename, 
                    u.username, 
                    SUM(mr.result) AS total_score
                FROM mocktestresults mr
                JOIN users u ON mr.user_id = u.user_id
                JOIN courses c ON mr.course_id = c.course_id
                GROUP BY c.coursename, u.username
                ORDER BY c.coursename, total_score DESC;
            """
            
            cursor.execute(query)
            results = cursor.fetchall()
            conn.close()

            leaderboard_data = {}
            user_positions = {}

            for course, username, total_score in results:
                if course not in leaderboard_data:
                    leaderboard_data[course] = []
                leaderboard_data[course].append([len(leaderboard_data[course]) + 1, username, total_score])

                # Store the position of the logged-in user
                if username == logged_in_user:
                    user_positions[course] = len(leaderboard_data[course])

            # Filter data: Top 5 + logged-in user (if they are outside top 5)
            filtered_data = {}
            for course, users in leaderboard_data.items():
                top_5 = users[:5]  # Get top 5 users

                if course in user_positions and user_positions[course] > 5:
                    # Find logged-in user's data
                    logged_user_data = next((x for x in users if x[1] == logged_in_user), None)
                    if logged_user_data:
                        logged_user_data = [user_positions[course]] + logged_user_data[1:]  # Update with actual position
                        top_5.append(logged_user_data)

                filtered_data[course] = top_5

            return filtered_data

        def create_table(frame, data):
            headers = ["SN", "Username", "Score"]
            for col, header in enumerate(headers):
                Label(frame, text=header, font=("Arial", 12, "bold"), bg="grey", width=10).grid(row=0, column=col, padx=1, pady=1)

            for row_idx, row_data in enumerate(data):
                for col_idx, value in enumerate(row_data):
                    Label(frame, text=value, font=("Arial", 12), bg="white", width=10, relief="ridge").grid(row=row_idx + 1, column=col_idx, padx=1, pady=1)

        
        header = Label(main_frame, text="Leaderboard", font=("Arial", 16, "bold"), bg="white")
        header.pack(pady=10)

        # Fetch and populate leaderboard
        data = fetch_leaderboard_data(LOGGED_IN_USER)

        positions = [(400, 135), (900, 135), (400, 525), (900, 525)]
        course_titles = list(data.keys())

        for i, course in enumerate(course_titles[:4]):  # Display up to 4 courses
            table_frame = Frame(main_frame, bd=2)
            table_frame.place(x=positions[i][0], y=positions[i][1], width=390, height=250)
            Label(main_frame, text=course, font=('Arial', 14, 'bold'), fg='black', bg='#E74C3C').place(x=positions[i][0], y=positions[i][1] - 35)
            create_table(table_frame, data[course])

        pass
    
    # Edit profile - user section - mukesh
    elif btn_text == "Profile":
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

        def update_profile_in_db(user_id, fullname, email, username, contact, address, password):
            """Update the user profile in the database."""
            try:
                conn = sqlite3.connect(DATABASE_FILE)
                c = conn.cursor()
                if password != None:
                    query = """
                    UPDATE users
                    SET fullname = ?, email = ?, username = ?, contact = ?, address = ?, password = ?
                    WHERE user_id = ?
                    """
                    c.execute(query, (fullname, email, username, contact, address, password, user_id))
                else:
                    query = """
                    UPDATE users
                    SET fullname = ?, email = ?, username = ?, contact = ?, address = ?
                    WHERE user_id = ?
                    """
                    c.execute(query, (fullname, email, username, contact, address, user_id))    
                
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
        print(users)
        
        header = Label(main_frame, text="Profile", font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10)
        
        secframe = Frame(main_frame, bd=2, relief='ridge')
        secframe.place(x=380, y=50, width=900, height=700)
         
        score = Label(main_frame, text='score:1500',font=('Arial',12)).place(x=780,y=225)
        
        profile = Label(main_frame, text='👦', font=('Arial',60)).place(x=775,y=110)
       
        username = Label(main_frame, text=users[3], font=('Arial', 14, 'bold')).place(x=770, y=255)


        # Labels and Entries
        labels_entries = [
            ("Name", 425, 320, users[1]),
            ("User Name", 425, 400, users[3]),
            ("Contact Number", 425, 480, users[4]),
            ("Email", 425, 560, users[2]),
            ("Address", 950, 480, users[5]),
            ("New Password", 950, 320, "",),
            ("Confirm Password", 950, 400, "")
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
        Button(main_frame,text='UPDATE', bg=BUTTON_COLOR, fg=FG_COLOR, font=('Arial', 14, 'bold'), command=update_profile).place(x=screen_width/2.5, y=690)

        pass
     
    # Course - usersection - Aayush
    elif btn_text == 'Courses':

        def create_page(container, text):
            """Creates a page with a label displaying the given text."""
            frame = ttk.Frame(container, style="TFrame")
            label = ttk.Label(frame, text=text, font=("Arial", 16), anchor="center", background="#f0f4f8", foreground="#003366")
            label.pack(expand=True, fill="both", padx=10, pady=10)
            return frame

            

        # Set styles
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="#003366", borderwidth=0)
        style.configure("TNotebook.Tab", background="#00509e", foreground="white", font=("Arial", 12, "bold"), padding=(10, 5))
        style.map("TNotebook.Tab", background=[("selected", "#003366")], foreground=[("selected", "white")])
        style.configure("TFrame", background="#f0f4f8")

        # Outer Notebook for Courses
        course_tabs = ttk.Notebook(main_frame)
        course_tabs.pack(expand=True, fill="both")

        # Sample Courses
        courses = {
            "CEE": ["Exam Pattern", "Questions", "Mock Test"],
            "IOE": ["Exam Pattern", "Questions", "Mock Test"],
            "Driving License Exam": ["Exam Pattern", "Questions", "Mock Test"],
            'Loksewa Exam' : ['Exam Pattern', 'Questions', 'Mock Test']
    }
        

        for course_name, topics in courses.items():
            # Create a tab for each course
            course_tab = ttk.Frame(course_tabs, style="TFrame")
            course_tabs.add(course_tab, text=course_name)

            # Inner Notebook for Topics
            topic_tabs = ttk.Notebook(course_tab)
            topic_tabs.pack(expand=True, fill="both")

            for topic_name in topics:
                # Create a tab for each topic under the course
                topic_tab = create_page(topic_tabs, f"Content for {topic_name}")
                topic_tabs.add(topic_tab, text=topic_name)

    # Mock Test - user section - Bivek
    elif btn_text == "Mock Test":
        header = Label(main_frame, text="Mock Test", font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10)

        
        ttk.Combobox(main_frame,values=[coursename[1] for coursename in get_courses()]).pack()


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

def logout():
    root.destroy()
    runpy.run_path(r'..\quizapp-tkinter\app\welcome.py')
    pass

# Logout Button
logout_btn = Button(sidebar, text="Logout", bg=LOGOUT_COLOR, fg=FG_COLOR, font=("Arial", 10, "bold"), width=20, height=2, bd=0,command=logout)
logout_btn.pack(side='bottom', pady=20)

# Main Content Frame
main_frame = Frame(root, bg=MAINFRAME_COLOR, padx=20, pady=20)
main_frame.pack(expand=True, fill='both')

# Initialize with Dashboard
openbutton("Dashboard")

root.mainloop()
