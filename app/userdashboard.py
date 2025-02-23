from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
from PIL import ImageTk, Image
import sqlite3
from random import *
import os
import runpy

# Read the user ID from the temporary file
try:
    with open("temp_user_id.txt", "r") as f:
        user_id = f.read().strip()
    os.remove("temp_user_id.txt")  # Clean up the temporary file
except FileNotFoundError:
    user_id = None
import pybase64
import re #For password validation.
import json

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

def get_mocktest():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM mocktests')
    mocktest = c.fetchall()
    conn.close()
    return mocktest

# Sidebar Frame
sidebar = Frame(root, bg=SIDEBAR_COLOR, width=200, height=600)
sidebar.pack(side='left', fill='y')

# Profile Image Placeholder
profile_img = Label(sidebar, text="Profile Image", bg='white', width=15, height=5)
profile_img.pack(pady=10)

# Username and Score
username_label = Label(sidebar, text=f"User ID: {user_id}", fg=FG_COLOR, bg=SIDEBAR_COLOR, font=label_font)
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
                btn_submitqotd.config(state=DISABLED, text="Correct!", bg="green",fg=FG_COLOR)
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
        
        def create_table(frame, data):

        
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
        def switch_frame(switchvalue):
            switchvalue = not switchvalue
            for widget in mocktest_frame.winfo_children():
                widget.destroy()
            update_frame(switchvalue)

        def update_frame(start_mock):
            global time_left, mock_running  # Track if mock test is running
            
            def start_mocktest():
                if selected_mocktest.get().isprintable():
                    nonlocal mocktestname 
                    mocktestname = selected_mocktest.get()
                    disable_sidebar()  # Disable sidebar when test starts
                    switch_frame(start_mock)
                else:
                    messagebox.showwarning(title='Invalid Data', message='Invalid Selection in Mock Test.')

            if start_mock:
                nonlocal mocktestname

                # Mock Test timer and header functions
                
                def get_mocktest_fulltime(mocktest_id):
                    conn = sqlite3.connect(DATABASE_FILE)
                    cursor = conn.cursor()
                    cursor.execute("SELECT mocktest_name, fulltime FROM mocktests WHERE mocktest_id = ?", (mocktest_id,))
                    result = cursor.fetchone()
                    conn.close()
                    return result if result else ("Unknown Test", 95)  # Default 95 minutes if not found

                def countdown():
                    global time_left, mock_running
                    if time_left > 0:
                        hours = time_left // 3600
                        minutes = (time_left % 3600) // 60
                        seconds = time_left % 60
                        mocktesttimer_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")
                        time_left -= 1
                        mocktesttimer_label.after(1000, countdown)
                    else:
                        time_up()

                def time_up():
                    # switch_frame(start_mock)
                    submit_test()
                    global mock_running
                    mock_running = False
                    # enable_sidebar()  # Enable sidebar when test ends
                    messagebox.showinfo("Time Up!", f"Your {mocktestname} time is over!")

                mocktest_name, fulltime = get_mocktest_fulltime(
                    next((mt[0] for mt in get_mocktest() if mt[1] == mocktestname), 1)
                )

                # # Question Functions
                # def get_questions():
                #     conn = sqlite3.connect(DATABASE_FILE)
                #     c = conn.cursor()
                #     c.execute()
                #     pass



                time_left = fulltime * 60  
                mock_running = True  # Mock test is active

                heading_frame = Frame(mocktest_frame, border=2, borderwidth=2)
                heading_frame.pack(fill='x')

                mocktestname_label = Label(heading_frame, text=mocktest_name, font=("Arial", 14, "bold"), bg="lightgray")
                mocktestname_label.pack(side='left', padx=10)

                mocktesttimer_label = Label(heading_frame, text="00:00:00", font=("Arial", 14, "bold"), fg="red", bg="lightgray")
                mocktesttimer_label.pack(side='right', padx=10)

                countdown()

                # Question part
                    

                # Question designs
                question_frame = Frame(mocktest_frame)
                question_frame.pack(fill='both', expand=True, pady=10)

                # Create scrollable frame
                canvas = Canvas(question_frame, bd=5, highlightthickness=0,height=screen_height)
                scroll_y = ttk.Scrollbar(question_frame, orient="vertical", command=canvas.yview)
                scroll_x = ttk.Scrollbar(question_frame, orient="horizontal", command=canvas.xview)
                canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

                # Pack scrollbars and canvas
                scroll_y.pack(side="right", fill="y")
                scroll_x.pack(side="bottom", fill="x")
                canvas.pack(side="left", fill="both", expand=True)

                # Inner frame for questions
                inner_frame = Frame(canvas)
                canvas.create_window((0,0), window=inner_frame, anchor="nw")

                # Configure scroll region
                def configure_scrollregion(event):
                    canvas.configure(scrollregion=canvas.bbox("all"))
                inner_frame.bind("<Configure>", configure_scrollregion)

                # Get questions from database
                def get_questions(mocktest_id):
                    conn = sqlite3.connect(DATABASE_FILE)
                    cursor = conn.cursor()
                    
                    # Get mocktest configuration
                    cursor.execute("SELECT course_id, category_id, no_of_questions FROM mockquestions WHERE mocktest_id=?", (mocktest_id,))
                    configs = cursor.fetchall()
                    
                    questions = []
                    for config in configs:
                        course_id, category_id, no_of_questions = config
                        # Get random questions for this category
                        cursor.execute("""SELECT question_id, question, correct_ans, incorrect_ans 
                                       FROM questions 
                                       WHERE course_id=? AND category_id=?
                                       ORDER BY RANDOM() LIMIT ?""", 
                                       (course_id, category_id, no_of_questions))
                        questions.extend(cursor.fetchall())
                    
                    conn.close()
                    return questions

                # Get mocktest ID
                mocktest_id = next((mt[0] for mt in get_mocktest() if mt[1] == mocktestname), 1)
                
                # Retrieve questions
                questions = get_questions(mocktest_id)
                user_answers = {}  # Store user's answers {question_id: answer}

                # Display questions
                for idx, (qid, question_text, correct, incorrect) in enumerate(questions, 1):
                    q_frame = Frame(inner_frame, relief="solid", padx=10, pady=10)
                    q_frame.pack(fill="x", pady=5, padx=5)
                    
                    Label(q_frame, text=f"Question {idx}: {question_text}", font=("Arial", 12), wraplength=700).pack(anchor="w")
                    
                    # Shuffle answer options
                    incorrect = json.loads(incorrect)
                    options = [correct] + incorrect
                    shuffle(options)
                    
                    # Radio buttons for options
                    var = StringVar()
                    user_answers[qid] = var
                    for opt in options:
                        Radiobutton(q_frame, text=opt, variable=var, value=opt, 
                                   font=("Arial", 11), wraplength=650).pack(anchor="w")

                # Submit button
                def submit_test():
                    # Calculate score
                    score = 0
                    total = len(questions)
                    for qid, correct in [(q[0], q[2]) for q in questions]:
                        if user_answers[qid].get() == correct:
                            score += 1
                    
                    # Get mocktest details
                    conn = sqlite3.connect(DATABASE_FILE)
                    cursor = conn.cursor()
                    cursor.execute("SELECT fullmark, passmark FROM mocktests WHERE mocktest_id=?", (mocktest_id,))
                    fullmark, passmark = cursor.fetchone()
                    
                    # Calculate percentage
                    percentage = (score / total) * 100 if total > 0 else 0
                    scaled_score = (score / total) * fullmark if total > 0 else 0
                    scaled_score = scaled_score
                    
                    # Save result (assuming current_user is available)
                    current_user_id = 1  # Replace with actual logged-in user ID
                    cursor.execute("""INSERT INTO mocktestresults 
                                   (mocktest_id, user_id, course_id, result, resulttime)
                                   VALUES (?, ?, ?, ?, datetime('now'))""",
                                   (mocktest_id, current_user_id, questions[0][0] if questions else 0, scaled_score))
                    conn.commit()
                    conn.close()
                    
                    # Show result
                    result_text = f"""Score: {scaled_score:.2f}/{fullmark}
                    Percentage: {percentage}
                    Correct Answers: {score}/{total}
                    Pass Status: {'Passed' if scaled_score >= passmark else 'Failed'}"""
                    switch_frame(start_mock)
                    enable_sidebar()
                    messagebox.showinfo("Test Results", result_text)

                submit_btn = Button(inner_frame, text="Submit Test", command=submit_test, 
                                  font=("Arial", 14, "bold"), bg="#4CAF50", fg="white")
                submit_btn.pack(pady=20)

            else:
                Label(mocktest_frame, text='Select a Mocktest and press start!', bg=MAINFRAME_COLOR, font=label_font).pack()

                selected_mocktest = StringVar(mocktest_frame, value=get_mocktest()[0][1])

                mocktest_combo = ttk.Combobox(mocktest_frame, values=[mocktestname[1] for mocktestname in get_mocktest()],
                                              textvariable=selected_mocktest, state='readonly')
                mocktest_combo.pack()

                mocktest_details = Label(mocktest_frame, font=button_font)
                mocktest_details.pack(padx=10, pady=10)
                mocktest_details.config(text=next((detail[2] for detail in get_mocktest() if detail[1] == selected_mocktest.get()), ""))

                start_button = Button(bg=BUTTON_COLOR, fg=FG_COLOR, text='Start', font=button_font,
                                      master=mocktest_frame, command=start_mocktest)
                start_button.pack(padx=10, pady=10)

        # 🔹 Functions to Lock and Unlock Sidebar
        def disable_sidebar():
            """Disable sidebar buttons to prevent navigation during the mock test."""
            for widget in sidebar.winfo_children():
                if isinstance(widget, Button):
                    widget.config(state=DISABLED)  # Disable all buttons

        def enable_sidebar():
            """Re-enable sidebar buttons after the mock test ends."""
            for widget in sidebar.winfo_children():
                if isinstance(widget, Button):
                    widget.config(state=NORMAL)  # Enable all buttons

        # def warn_sidebar_access():
        #     """Warn user when they try to click the sidebar during the test."""
        #     if mock_running:
        #         m = messagebox.askyesno("Warning", "You surely want to leave the test while it's running!\nAll done will get lost.")
        #         if m:
        #             enable_sidebar()


        # # Attach warning function to sidebar buttons
        # for widget in sidebar.winfo_children():
        #     if isinstance(widget, Button):
        #         widget.config(command=lambda: warn_sidebar_access())

        # Initialize test state
        start_mock = False
        mock_running = False  # Track if mock test is running
        mocktestname = ''

        header = Label(main_frame, text="Mock Test", font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10,fill='x')

        mocktest_frame = Frame(main_frame, border=5, borderwidth=5, padx=10, pady=10)
        mocktest_frame.pack(fill='both')

        update_frame(start_mock)

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

# Logout Button
logout_btn = Button(sidebar, text="Logout", bg=LOGOUT_COLOR, fg=FG_COLOR, font=("Arial", 10, "bold"), width=20, height=2, bd=0,command=logout)
logout_btn.pack(side='bottom', pady=20)

# Main Content Frame
main_frame = Frame(root, bg=MAINFRAME_COLOR, padx=20, pady=20)
main_frame.pack(expand=True, fill='both')

# Initialize with Dashboard
openbutton("Dashboard")

root.mainloop()