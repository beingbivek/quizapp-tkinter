import ast
from tkinter import *
from tkinter import ttk, messagebox
import os, re, json, sqlite3
from random import *
from PIL import ImageTk

# User window
root = Tk()
root.configure(bg="white")
root.attributes("-fullscreen", True)

# Importing defaults after root creation
from quizdefaults import *


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.title("Quiz App - User Dashboard")
root.configure(bg=MAINFRAME_COLOR)

# Making close and minimize button manually
minclose_windowbtn(root)

# Functions

# Read the user details from the temporary file
try:
    if not os.path.exists(USER_FILE):
        messagebox.showerror('Error', 'User session file not found. Please log in again.')
        back_to_welcome(root)

    with open(USER_FILE, "r") as f:
        LOGGED_IN_USER = ast.literal_eval(f.read().strip()) # Read entire file content
    os.remove(USER_FILE)  # Clean up the temporary file
except FileNotFoundError:
    messagebox.showerror('File Error','User File not found.')
    LOGGED_IN_USER = None

# Fail Safe
if not LOGGED_IN_USER or len(LOGGED_IN_USER) < 9:
    messagebox.showerror('Error', 'Invalid user data. Please log in again.')
    back_to_welcome(root)
    
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

# get user scores
def total_score_of_user(user_id):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(result) FROM mocktestresults WHERE user_id = ?", (user_id,))
        total_score = cursor.fetchone()[0]

        conn.close()

        return total_score if total_score is not None else 0  # Return 0 if no results found

    except sqlite3.Error as e:
        messagebox.showerror("Database error:", f'Error is: {e}')
        return 0

# Sidebar Frame
sidebar = Frame(root, bg=SIDEBAR_COLOR, width=200, height=600)
sidebar.pack(side='left', fill='y')

# Profile Image Placeholder
profile_image = ImageTk.PhotoImage(file=ICON_FILE_WHITE)
profile_img = Label(sidebar, image=profile_image,height=100,width=100, bg=SIDEBAR_COLOR)
profile_img.pack()

# Username and Score
username_label = Label(sidebar, text=f"{LOGGED_IN_USER[1]}", fg=FG_COLOR, bg=SIDEBAR_COLOR, font=label_font)
username_label.pack()

score_label = Label(sidebar, text=f"Score: {total_score_of_user(LOGGED_IN_USER[0])}", fg=FG_COLOR, bg=SIDEBAR_COLOR, font=("Arial", 10))
score_label.pack()

# Store button references
buttons = {}

# Sidebar Button Function
def openbutton(btn_text):
    # Update username label if updated
    username_label.config(text=LOGGED_IN_USER[1])
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
        current_user_id = LOGGED_IN_USER[0]

        try:
            # Connect to database
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()

            # Fetch Random Question for "Question of the Day"
            cursor.execute("SELECT question_id, question, correct_ans, incorrect_ans, course_id, category_id FROM questions ORDER BY RANDOM() LIMIT 1")
            qotd_data = cursor.fetchone()
            if not qotd_data:
                messagebox.showerror('No Question','There\'s no question in Database so, replace with dummy one.')
                qotd_data = dummyquestion
        except Exception as e:
            messagebox.showerror

        question_id, question_text, correct_answer, incorrect_answers, course_id, category_id = qotd_data

        # Parse incorrect answers stored as JSON list
        incorrect_answers = json.loads(incorrect_answers)
        options = incorrect_answers + [correct_answer]
        shuffle(options)

        def question_location():
            try:
                coursename = next((name[1] for name in get_courses() if course_id == name[0]),"Random")
                categoryname = next((name[1] for name in get_categories() if category_id == name[0]),"Question")
                return coursename + ' ' + categoryname
            except:
                messagebox.showerror('No course and categories','There is no course and category data in database.')
                return 'No Database connection, Solve This'

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
                btn_submitqotd.config(state=DISABLED, text="Correct!", bg="green",font=button_font)
            else:
                btn_submitqotd.config(text="Try Again", bg="red",font=button_font)

        for opt in options:
            rb = Radiobutton(main_frame, text=opt, variable=selected_option, value=opt, bg=MAINFRAME_COLOR)
            rb.pack(anchor='w')
            option_buttons.append(rb)

        btn_submitqotd = Button(main_frame, text='Submit', bg=BUTTON_COLOR, command=check_answer, font=button_font,fg=FG_COLOR)
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

        progress_data = fetch_progress_data(current_user_id)
        for i, row in enumerate(progress_data, start=1):
            progress_table.insert('', 'end', values=(i, *row))
        progress_table.pack()

        # Build Mock Table results

        mocktestresult_table(main_frame,LOGGED_IN_USER[0])

        
    #Leaderboard user section.    
    elif btn_text == "LeaderBoard":

        # Fetch leaderboard data
        def fetch_leaderboard_data(logged_in_user_id):
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    c.coursename, 
                    u.user_id, 
                    u.username, 
                    SUM(mr.result) AS total_score
                FROM mocktestresults mr
                JOIN users u ON mr.user_id = u.user_id
                JOIN courses c ON mr.course_id = c.course_id
                GROUP BY c.coursename, u.user_id
                ORDER BY c.coursename, total_score DESC;
            """
            
            cursor.execute(query)
            results = cursor.fetchall()
            conn.close()

            leaderboard_data = {}
            user_positions = {}

            for course, user_id, username, total_score in results:
                if course not in leaderboard_data:
                    leaderboard_data[course] = []
                leaderboard_data[course].append([len(leaderboard_data[course]) + 1, username, total_score])

                # Store the position of the logged-in user
                if user_id == logged_in_user_id:
                    user_positions[course] = len(leaderboard_data[course])

            # Filter data: Top 5 + logged-in user (if they are outside top 5)
            filtered_data = {}
            for course, users in leaderboard_data.items():
                top_5 = users[:5]  # Get top 5 users

                if course in user_positions and user_positions[course] > 5:
                    # Find logged-in user's data
                    logged_user_data = next((x for x in users if x[1] == logged_in_user_id), None)
                    if logged_user_data:
                        logged_user_data = [user_positions[course]] + logged_user_data[1:]  # Update with actual position
                        top_5.append(logged_user_data)

                filtered_data[course] = top_5

            return filtered_data

        # Create a scrollable table using Treeview
        def create_table(frame, data, course_name):
            # Course title
            title_label = Label(frame, text=course_name, font=("Arial", 14, "bold"), fg="black", bg=MAINFRAME_COLOR)
            title_label.pack(pady=5)

            # Create a Treeview widget
            tree = ttk.Treeview(frame, columns=("SN", "Username", "Score"), show="headings")
            tree.heading("SN", text="SN")
            tree.heading("Username", text="Username")
            tree.heading("Score", text="Score")
            tree.column("SN", width=50, anchor="center")
            tree.column("Username", width=150, anchor="center")
            tree.column("Score", width=100, anchor="center")

            # Insert data into the Treeview
            for row in data:
                tree.insert("", "end", values=row)

            # Add a vertical scrollbar for the table
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            tree.pack(side="left", fill="both", expand=True)

        # Main application
        # Header
        header = Label(main_frame, text="Leaderboard", font=("Arial", 16, "bold"), bg=MAINFRAME_COLOR)
        header.pack(pady=10)

        # Fetch leaderboard data
        data = fetch_leaderboard_data(LOGGED_IN_USER[0])

        # Create a Canvas for scrollable content
        canvas = Canvas(main_frame, bg=MAINFRAME_COLOR)
        canvas.pack(side="left", fill="both", expand=True)

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame to hold all tables
        table_container = Frame(canvas, bg=MAINFRAME_COLOR)
        canvas.create_window((0, 0), window=table_container, anchor="nw")

        # Function to update scroll region
        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        table_container.bind("<Configure>", update_scroll_region)

        # Display all leaderboard tables (2 per row)
        courses = list(data.keys())
        for i in range(0, len(courses), 2):
            row_frame = Frame(table_container, bg="white")
            row_frame.pack(fill="x", pady=10)

            # First table in the row
            if i < len(courses):
                course1 = courses[i]
                table_frame1 = Frame(row_frame, bd=2, relief="groove")
                table_frame1.pack(side="left", fill="both", expand=True, padx=10)
                create_table(table_frame1, data[course1], course1)

            # Second table in the row
            if i + 1 < len(courses):
                course2 = courses[i + 1]
                table_frame2 = Frame(row_frame, bd=2, relief="groove")
                table_frame2.pack(side="left", fill="both", expand=True, padx=10)
                create_table(table_frame2, data[course2], course2)
    
    # Edit profile - user section - mukesh
    elif btn_text == "Profile":
        # Edit profile Functions - mukesh
        if len(LOGGED_IN_USER) < 8:
            messagebox.showerror('Profile Error','Missing profile data')
            return

        def update_profile_in_db(user_id, fullname, email, username, contact, address, password, sq, sq_answer):
            """Update the user profile in the database."""
            try:
                update_successful = False
                conn = sqlite3.connect(DATABASE_FILE)
                c = conn.cursor()
                if password and sq_answer:
                    try:
                        query = """
                        UPDATE users
                        SET fullname = ?, email = ?, username = ?, contact = ?, address = ?, password = ?, securityquestion = ?, securityanswer = ?
                        WHERE user_id = ?
                        """
                        c.execute(query, (fullname, email, username, contact, address, password, sq, sq_answer, user_id))
                        update_successful = True
                    except Exception as e:
                        messagebox.showerror('Error',f'Error in updating user: {e}')
                elif sq_answer:
                    try:
                        query = """
                        UPDATE users
                        SET fullname = ?, email = ?, username = ?, contact = ?, address = ?, securityquestion = ?, securityanswer = ?
                        WHERE user_id = ?
                        """
                        c.execute(query, (fullname, email, username, contact, address, sq, sq_answer, user_id))
                        update_successful = True
                    except Exception as e:
                        messagebox.showerror('Error',f'Error in updating user: {e}')
                elif password:
                    try:
                        query = """
                        UPDATE users
                        SET fullname = ?, email = ?, username = ?, contact = ?, address = ?, password = ?, securityquestion = ?
                        WHERE user_id = ?
                        """
                        c.execute(query, (fullname, email, username, contact, address, password, sq, user_id))
                        update_successful = True
                    except Exception as e:
                        messagebox.showerror('Error',f'Error in updating user: {e}')
                else:
                    try:
                        query = """
                        UPDATE users
                        SET fullname = ?, email = ?, username = ?, contact = ?, address = ?, securityquestion = ?
                        WHERE user_id = ?
                        """
                        c.execute(query, (fullname, email, username, contact, address, sq, user_id))   
                        update_successful = True
                    except Exception as e:
                        messagebox.showerror('Error',f'Error in updating user: {e}')
                if update_successful:
                    c.execute('SELECT * FROM users where user_id = ?',(user_id,)) 
                    global LOGGED_IN_USER
                    LOGGED_IN_USER = list(c.fetchone())
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Profile updated successfully!")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")

        def validate_password(password):
            # Password must contain at least 1 uppercase letter, 1 lowercase letter, and 1 symbol
            if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[\W_]).+$', password,):
                return False
            return True

        def update_profile():
            if sq_answer_entry:
                value = sq_answer_entry.get().strip()
            else:
                value = 'None'
            updated_values = [entry.get().strip() for entry in entries] + [sq.get().strip(),value]
            print(updated_values)
            fullname, username, contact, email, address, new_password, confirm_password, sec_que, sec_que_answer = updated_values

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
                password = str_encode(new_password)
            else:
                # If password fields are empty, set password to None (do not update password)
                password = None

            # Checking for security questions
            if sec_que_answer != 'None':
                sec_que_answer = str_encode(sec_que_answer)
                # Check if the question is same
                if sec_que == users[7] and sec_que_answer == users[8]:
                    sec_que_answer = None
            else:
                sec_que_answer = None

            # Ask for confirmation
            confirm = messagebox.askyesno("Confirm Update", "Are you sure you want to update your profile?")
            if confirm:
                # Update the profile in the database
                update_profile_in_db(
                    user_id=users[0], 
                    fullname=fullname,
                    email=email,
                    username=username,
                    contact=contact,
                    address=address,
                    password=password,
                    sq=sec_que,
                    sq_answer=sec_que_answer
                )

        # Load user profile data
        users = LOGGED_IN_USER
        
        header = Label(main_frame, text="Profile", font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10)
        
        secframe = Frame(main_frame, bd=2, relief='ridge')
        secframe.place(x=380, y=50, width=900, height=700)

        score = Label(main_frame, text=f'Score:{total_score_of_user(users[0])}',font=('Arial',12)).place(x=780,y=225)
        
        profile = Label(main_frame, text='👦', font=('Arial',60)).place(x=775,y=110)
       
        label_username = Label(main_frame, text=users[3], font=('Arial', 14, 'bold')).place(x=770, y=255)

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
            entry.insert(0, str(value))
            entries.append(entry)

        # Security Question Part
        sq = StringVar()
        sq.set(users[7])
        # Label(main_frame, text="Select Security Question:", bg='white', fg='black').place(x=250, y=90)
        Label(main_frame, text='Change Security Question').place(x=950, y=540)
        OptionMenu(main_frame, sq, *security_questions).place(x=950, y=560)

        Label(main_frame, text='New Security Answer').place(x=950, y=600)
        sq_answer_entry = Entry(main_frame, width=35).place(x=950,y=620)

        # Buttons
        Button(main_frame,text='UPDATE', bg=BUTTON_COLOR, fg=FG_COLOR, font=('Arial', 14, 'bold'), command=update_profile).place(x=screen_width/2.5, y=700)
     
    # Course - usersection - Aayush
    elif btn_text == 'Courses':

        def fetch_questions(course_id, category_id=None):
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            if category_id:
                cursor.execute("""
                    SELECT question, correct_ans
                    FROM questions
                    WHERE course_id = ? AND category_id = ?
                """, (course_id, category_id))
            else:
                cursor.execute("""
                    SELECT question, correct_ans
                    FROM questions
                    WHERE course_id = ?
                """, (course_id,))
            questions = cursor.fetchall()
            conn.close()
            return questions

        # Fetch categories for a course
        def fetch_categories(course_id):
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT category_id, category_name
                FROM categories
                WHERE course_id = ?
            """, (course_id,))
            categories = cursor.fetchall()
            conn.close()
            return categories

        # Display course description
        def show_course_description(course_desc, frame_bottom2_inner, frame_bottom2_canvas):
            # Clear the existing content in the inner frame
            for widget in frame_bottom2_inner.winfo_children():
                widget.destroy()

            # Display the course description
            label = Label(frame_bottom2_inner, text=course_desc, font=("Arial", 12), wraplength=500, justify="left",bg="#f0f4f8")
            label.pack(pady=10, padx=10, fill="both", expand=True)

            # Update scroll region after content is added
            frame_bottom2_inner.update_idletasks()
            frame_bottom2_canvas.config(scrollregion=frame_bottom2_canvas.bbox("all"))

        # Display questions for the selected category
        def show_questions(course_id, category_name, frame_bottom2_inner, frame_bottom2_canvas):
            # Clear the existing content in the inner frame
            for widget in frame_bottom2_inner.winfo_children():
                widget.destroy()

            # Fetch questions based on the selected category
            if category_name == "All":
                questions = fetch_questions(course_id)
            else:
                categories = fetch_categories(course_id)
                category_id = next((cat[0] for cat in categories if cat[1] == category_name), None)
                questions = fetch_questions(course_id, category_id)

            # Display the questions
            for question, correct_ans in questions:
                question_frame = Frame(frame_bottom2_inner, bd=2, relief="groove")
                question_frame.pack(fill="x", pady=5, padx=10)

                question_label = Label(question_frame, text=f"Q: {question}", font=("Arial", 12), anchor="w")
                question_label.pack(fill="x", padx=5, pady=2)

                answer_label = Label(question_frame, text=f"Correct Answer: {correct_ans}", font=("Arial", 12), anchor="w", fg="green")
                answer_label.pack(fill="x", padx=5, pady=2)

            # Update scroll region after content is added
            frame_bottom2_inner.update_idletasks()
            frame_bottom2_canvas.config(scrollregion=frame_bottom2_canvas.bbox("all"))


        # Handle course button click
        def on_course_button_click(course_id, course_desc, frame_bottom1, frame_bottom2_inner, frame_bottom2_canvas):
            # Clear the existing content in frame_bottom1
            for widget in frame_bottom1.winfo_children():
                widget.destroy()

            # Add a button to show course description
            desc_button = Button(frame_bottom1, text="Show Course Description",
                                    command=lambda: show_course_description(course_desc, frame_bottom2_inner, frame_bottom2_canvas),font=button_font,bg=BUTTON_COLOR,fg=FG_COLOR)
            desc_button.pack(side="left", padx=10, pady=10)

            # Fetch categories for the course
            categories = fetch_categories(course_id)
            category_names = ["All"] + [cat[1] for cat in categories]

            Label(frame_bottom1, text='Select a category:',font=button_font,bg="#f0f4f8").pack(side='left',padx=10,pady=10)

            # Add a dropdown for categories
            category_var = StringVar(value="All")
            category_dropdown = ttk.Combobox(frame_bottom1, textvariable=category_var, values=category_names, state="readonly",font=button_font)
            category_dropdown.pack(side="left", padx=10, pady=10)

            # Add a button to show questions
            show_questions_button = Button(frame_bottom1, text="Show Questions",
                                            command=lambda: show_questions(course_id, category_var.get(), frame_bottom2_inner, frame_bottom2_canvas),font=button_font,bg=BUTTON_COLOR,fg=FG_COLOR)
            show_questions_button.pack(side="left", padx=10, pady=10)

        # Fetch courses from the database
        courses = get_courses()

        # Header
        header = Label(main_frame, text="Courses", font=("Arial", 20, "bold"), bg=MAINFRAME_COLOR)
        header.pack(pady=10)

        Label(main_frame, text="Select a course, click Show Course Description to know about the course and get it's questions.", font=("Arial", 12, "bold"), bg=MAINFRAME_COLOR).pack(pady=10)

        # Upper Frame: Course Buttons with horizontal scrolling
        upper_frame_canvas = Canvas(main_frame, bg="#f0f4f8", highlightthickness=0)
        upper_frame_canvas.pack(fill="x", pady=10, side="top")
        upper_frame = Frame(upper_frame_canvas, bg="#f0f4f8")
        upper_frame_canvas.create_window((0, 0), window=upper_frame, anchor="nw")

        # Horizontal scrollbar for upper frame
        x_scrollbar = Scrollbar(upper_frame_canvas, orient="horizontal", command=upper_frame_canvas.xview)
        upper_frame_canvas.configure(xscrollcommand=x_scrollbar.set, xscrollincrement='1')
        x_scrollbar.pack(side="top", fill="x",pady=50)
        upper_frame_canvas.configure(yscrollcommand=lambda *args: None) # Disable vertical scrolling for upper frame

        for course_id, course_name, course_desc in courses:
            course_button = Button(upper_frame, text=course_name,
                                        command=lambda cid=course_id, desc=course_desc:
                                        on_course_button_click(cid, desc, frame_bottom1, frame_bottom2_inner, frame_bottom2_canvas),font=button_font,bg=BUTTON_COLOR,fg=FG_COLOR)
            course_button.pack(side="left", padx=10, pady=10)

        upper_frame.update_idletasks()
        upper_frame_canvas.config(scrollregion=upper_frame_canvas.bbox("all"))
        upper_frame_canvas.config(width=main_frame.winfo_width()) # Adjust width if needed


        # Bottom Frame: Divided into two sub-frames
        bottom_frame = Frame(main_frame, bg="#f0f4f8")
        bottom_frame.pack(fill="both", expand=True, side="top")

        # Frame Bottom 1: Course Description Button and Category Dropdown
        global frame_bottom1
        frame_bottom1 = Frame(bottom_frame, bg="#f0f4f8")
        frame_bottom1.pack(fill="x", pady=10)

        # Frame Bottom 2: Display Course Description or Questions with vertical scrolling
        frame_bottom2_canvas = Canvas(bottom_frame, bg="#f0f4f8", highlightthickness=0)
        frame_bottom2_canvas.pack(fill="both", expand=True)
        frame_bottom2_inner = Frame(frame_bottom2_canvas, bg="#f0f4f8")
        frame_bottom2_canvas.create_window((0, 0), window=frame_bottom2_inner, anchor="nw")

        # Vertical scrollbar for bottom frame 2
        y_scrollbar = Scrollbar(frame_bottom2_canvas, orient="vertical", command=frame_bottom2_canvas.yview)
        frame_bottom2_canvas.configure(yscrollcommand=y_scrollbar.set, yscrollincrement='1')
        y_scrollbar.pack(side="right", fill="y")
        frame_bottom2_canvas.configure(xscrollcommand=lambda *args: None) # Disable horizontal scrolling for bottom frame 2


        global frame_bottom2_inner_global
        frame_bottom2_inner_global = frame_bottom2_inner
        global frame_bottom2_canvas_global
        frame_bottom2_canvas_global = frame_bottom2_canvas

        # Show description of the first course by default
        if courses:
            first_course_id, first_course_name, first_course_desc = courses[0]
            on_course_button_click(first_course_id, first_course_desc, frame_bottom1, frame_bottom2_inner, frame_bottom2_canvas)
            show_course_description(first_course_desc, frame_bottom2_inner, frame_bottom2_canvas) # Directly show description

    # Mock Test - user section - Bivek
    elif btn_text == "Mock Test":
        def switch_frame(switchvalue):
            switchvalue = not switchvalue
            for widget in mocktest_frame.winfo_children():
                widget.destroy()
            # update score:
            score_label.config(text=f"Score: {total_score_of_user(LOGGED_IN_USER[0])}")
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
                    
                    # Save result (assuming current_user is available)
                    current_user_id = LOGGED_IN_USER[0]
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

                # Build Mock Table results

                mocktestresult_table(mocktest_frame,LOGGED_IN_USER[0])

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

# Logout Button
logout_btn = Button(sidebar, text="Logout", bg=LOGOUT_COLOR, fg=FG_COLOR, font=("Arial", 10, "bold"), width=20, height=2, bd=0,command=lambda: logout(root))
logout_btn.pack(side='bottom', pady=20)

# Main Content Frame
main_frame = Frame(root, bg=MAINFRAME_COLOR, padx=20, pady=20)
main_frame.pack(expand=True, fill='both')

# Initialize with Dashboard
openbutton("Dashboard")

root.mainloop()