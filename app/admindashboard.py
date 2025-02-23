from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
from PIL import ImageTk, Image
import runpy
import sqlite3
from tkinter import simpledialog
import tkinter as tk
import json

# Admin Window
root = Tk()
root.configure(bg="white")
root.attributes("-fullscreen", True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.title("Quiz App - Admin Dashboard")

# Importing defaults after root creation
from quizdefaults import *

root.configure(bg=MAINFRAME_COLOR)

# making close and minimize button manually
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
btn2 = Button(root, text="✕", command=max, width=4, bg=HEADER_COLOR, border=0, font=font.Font(size=14))
btn2.pack(anchor="ne")
btn2.bind('<Enter>', on_enter)
btn2.bind('<Leave>', on_leave)

btn = Button(root, text="-", command=min, width=4, bg=HEADER_COLOR, border=0, font=font.Font(size=14))
btn.place(x=screen_width-100, y=0)

def enter(i):
    btn['background'] = "red"

def leave(i):
    btn['background'] = HEADER_COLOR

btn.bind('<Enter>', enter)
btn.bind('<Leave>', leave)

# Store button references
buttons_dict = {}

# Sidebar button functions
def openbutton(btn_text):
    # Clear the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Reset all button colors
    for btn in buttons_dict.values():
        btn.configure(bg=BUTTON_COLOR)

    # Set the clicked button color
    buttons_dict[btn_text].configure(bg=HIGHLIGHT_COLOR)

    if btn_text == buttons[0]:
        # Main Dashboard
        header = Label(main_frame, text="Dashboard", font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10)

        stats_frame = Frame(main_frame, bg=MAINFRAME_COLOR)
        stats_frame.pack()

        # Stat data
        stat_data = [("123", "Total Users"), ("4", "Total Courses"), ("123", "Total Subcategories"), ("123", "Total Questions")]

        for stat in stat_data:
            stat_box = Frame(stats_frame, bg=BUTTON_COLOR, width=120, height=60)
            stat_box.pack_propagate(False)
            stat_box.pack(side=LEFT, padx=10, pady=10)
            
            stat_label = Label(stat_box, text=stat[0], font=("Arial", 14, "bold"), fg=FG_COLOR, bg=BUTTON_COLOR)
            stat_label.pack()
            stat_desc = Label(stat_box, text=stat[1], font=("Arial", 10), fg=FG_COLOR, bg=BUTTON_COLOR)
            stat_desc.pack()

        # Table Data
        table_frame = Frame(main_frame)
        table_frame.pack(pady=20)

        columns = ("Particulars", "Numbers", "Remark")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=CENTER, width=150)

        tree.insert("", "end", values=("User Registered Today", "56", "Grown by 10%"))
        tree.insert("", "end", values=("Mock Test Today", "50", "Grown by 10%"))

        tree.pack()

    # user - admin section

    elif btn_text == buttons[1]:
        # Clear the main frame
        for widget in main_frame.winfo_children():
            widget.destroy()

        # Colors
        bgcolor = "#E0E0E0"
        button_color = "#34495E"
        accent_color = "#1F618D"
        delete_color = "#E74C3C"

        # Header
        header = Label(main_frame, text="Users", font=("Arial", 16, "bold"), bg=MAINFRAME_COLOR)
        header.place(relx=0.05, rely=0.02)

        # Stats section
        stats_frame = Frame(main_frame, bg=MAINFRAME_COLOR)
        stats_frame.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.1)

        stat_data = [("123", "Total Users")]
        for i, stat in enumerate(stat_data):
            stat_box = Frame(stats_frame, bg=button_color, width=120, height=60)
            stat_box.place(relx=i * 0.3, rely=0, relwidth=0.2, relheight=1)

            stat_label = Label(stat_box, text=stat[0], font=("Arial", 14, "bold"), fg="white", bg=button_color)
            stat_label.place(relx=0.5, rely=0.3, anchor=CENTER)
            stat_desc = Label(stat_box, text=stat[1], font=("Arial", 10), fg="white", bg=button_color)
            stat_desc.place(relx=0.5, rely=0.7, anchor=CENTER)

        # Add User Button
        add_button = Button(stats_frame, text="Add User", bg=accent_color, fg="black", relief=FLAT, command=lambda: register_user())
        add_button.place(relx=0.8, rely=0.2, relwidth=0.15, relheight=0.6)

        # User display options
        no_of_user = ["3", "6", "9", "12"]
        selected_user_no = StringVar(value="No. of user displayed")
        user_dropdown = OptionMenu(main_frame, selected_user_no, *no_of_user, command=lambda x: user_no_selected(x))
        user_dropdown.config(font=("Arial", 10), width=13)
        user_dropdown.place(relx=0.05, rely=0.25)

        # Filter options
        filter_value = ["Username", "SN"]
        filter_with = StringVar(value="Filter With:")
        filter_dropdown = OptionMenu(main_frame, filter_with, *filter_value, command=lambda x: filter_info(x))
        filter_dropdown.config(font=("Arial", 10), width=13)
        filter_dropdown.place(relx=0.25, rely=0.25)

        # Search Bar
        search_label = Label(main_frame, text="Search:", font=("Arial", 13), bg=MAINFRAME_COLOR, fg='black')
        search_label.place(relx=0.45, rely=0.25)

        search_entry = Entry(main_frame, font=("Arial", 10), width=20)
        search_entry.place(relx=0.52, rely=0.25)

        search_button = Button(main_frame, text="Search", bg=accent_color, fg="black", relief=FLAT, command=lambda: search_table())
        search_button.place(relx=0.72, rely=0.25, width=80)

        # Table
        table_frame = Frame(main_frame, bg=MAINFRAME_COLOR)
        table_frame.place(relx=0.05, rely=0.35, relwidth=0.9, relheight=0.5)

        columns = ("Sn", "Username", "Name", "Contact", "Email")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=CENTER, width=150)

        # Sample data
        rows = [
            ("1", "poplol2", "Ram Rai", "9876543210", "a@gmail.com"),
            ("2", "user123", "John Doe", "1234567890", "john@example.com"),
            ("3", "testuser", "Jane Doe", "0987654321", "jane@example.com")
        ]

        for row in rows:
            tree.insert("", "end", values=row)

        tree.configure(height=len(rows))
        tree.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Action Buttons
        edit_button = Button(main_frame, text="Edit", bg=accent_color, fg="black", relief=FLAT, command=lambda: edit_user())
        edit_button.place(relx=0.05, rely=0.9, relwidth=0.1, relheight=0.05)

        delete_button = Button(main_frame, text="Delete", bg=delete_color, fg="black", relief=FLAT, command=lambda: delete_user())
        delete_button.place(relx=0.15, rely=0.9, relwidth=0.1, relheight=0.05)

        # Functions
        def user_no_selected(selected_user_no):
            for row in tree.get_children():
                tree.delete(row)

            num_rows = int(selected_user_no)
            for i in range(min(num_rows, len(rows))):
                tree.insert("", "end", values=rows[i])

            tree.configure(height=num_rows)

        def filter_info(filter_with):
            for row in tree.get_children():
                tree.delete(row)

            if filter_with == "Username":
                sorted_rows = sorted(rows, key=lambda x: x[1].lower())
            elif filter_with == "SN":
                sorted_rows = sorted(rows, key=lambda x: int(x[0]))
            else:
                sorted_rows = rows

            for row in sorted_rows:
                tree.insert("", "end", values=row)

            tree.configure(height=len(sorted_rows))

        def search_table():
            search_term = search_entry.get().strip().lower()

            for row in tree.get_children():
                tree.delete(row)

            filtered_rows = [row for row in rows if any(search_term in str(cell).lower() for cell in row)]

            for row in filtered_rows:
                tree.insert("", "end", values=row)

            tree.configure(height=len(filtered_rows))

        def register_user():
            register_window = Toplevel(root)
            register_window.title("Register User")
            register_window.geometry("400x300")

            Label(register_window, text="Username:").place(relx=0.1, rely=0.1)
            username_entry = Entry(register_window)
            username_entry.place(relx=0.3, rely=0.1)

            Label(register_window, text="Name:").place(relx=0.1, rely=0.2)
            name_entry = Entry(register_window)
            name_entry.place(relx=0.3, rely=0.2)

            Label(register_window, text="Contact:").place(relx=0.1, rely=0.3)
            contact_entry = Entry(register_window)
            contact_entry.place(relx=0.3, rely=0.3)

            Label(register_window, text="Email:").place(relx=0.1, rely=0.4)
            email_entry = Entry(register_window)
            email_entry.place(relx=0.3, rely=0.4)

            Button(register_window, text="Submit", command=lambda: submit_registration(
                username_entry.get(), name_entry.get(), contact_entry.get(), email_entry.get(), register_window
            )).place(relx=0.4, rely=0.6)

        def submit_registration(username, name, contact, email, window):
            new_user = (str(len(rows) + 1), username, name, contact, email)
            rows.append(new_user)
            tree.insert("", "end", values=new_user)
            window.destroy()

        def edit_user():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select a user to edit.")
                return

            selected_user = tree.item(selected_item, "values")
            edit_window = Toplevel(root)
            edit_window.title("Edit User")
            edit_window.geometry("400x300")

            Label(edit_window, text="Username:").place(relx=0.1, rely=0.1)
            username_entry = Entry(edit_window)
            username_entry.insert(0, selected_user[1])
            username_entry.place(relx=0.3, rely=0.1)

            Label(edit_window, text="Name:").place(relx=0.1, rely=0.2)
            name_entry = Entry(edit_window)
            name_entry.insert(0, selected_user[2])
            name_entry.place(relx=0.3, rely=0.2)

            Label(edit_window, text="Contact:").place(relx=0.1, rely=0.3)
            contact_entry = Entry(edit_window)
            contact_entry.insert(0, selected_user[3])
            contact_entry.place(relx=0.3, rely=0.3)

            Label(edit_window, text="Email:").place(relx=0.1, rely=0.4)
            email_entry = Entry(edit_window)
            email_entry.insert(0, selected_user[4])
            email_entry.place(relx=0.3, rely=0.4)

            Button(edit_window, text="Submit", command=lambda: submit_edit(
                selected_item, username_entry.get(), name_entry.get(), contact_entry.get(), email_entry.get(), edit_window
            )).place(relx=0.4, rely=0.6)

        def submit_edit(selected_item, username, name, contact, email, window):
            for i, row in enumerate(rows):
                if row[0] == tree.item(selected_item, "values")[0]:
                    rows[i] = (row[0], username, name, contact, email)
                    break

            tree.item(selected_item, values=(rows[i]))
            window.destroy()

        def delete_user():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select a user to delete.")
                return

            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?"):
                selected_user = tree.item(selected_item, "values")
                global rows
                rows = [row for row in rows if row[0] != selected_user[0]]
                tree.delete(selected_item)

    # Courses - admin section - bivek
    elif btn_text == buttons[2]:

        def on_entry_click(event):
            # Function to remove placeholder text when the entry is clicked.
            if search_entry.get() == 'Search...':
                search_entry.delete(0, "end")  # delete all the text in the entry
                search_entry.insert(0, '')  # Insert blank for user input
                search_entry.config(fg='black')

        def on_focusout(event):
            # Function to add placeholder text if the entry is empty when focus is lost.
            if search_entry.get() == '':
                search_entry.insert(0, 'Search...')
                search_entry.config(fg='grey')
                # display all courses after the search bar is empty
                update_table(courses)

        def search_courses():
            query = f'SELECT * FROM courses WHERE coursename LIKE ?'
            # query = f'SELECT * FROM courses'
            search_term = f'%{search_entry.get()}%'
            # c.execute(query)
            c.execute(query, (search_term,))
            results = c.fetchall()
            # print(results)
            
            # show the search result
            update_table(results)

        def update_table(results):
            for row in table.get_children():
                table.delete(row)
            for row in results:
                table.insert('', 'end', values=row)

        # Database Connection
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()

        # demo courses creation or insertion
        c.execute('SELECT * FROM courses')
        cou = c.fetchall()
        if not cou:
            for cn in defcourses:
                c.execute('INSERT INTO courses (coursename) VALUES (?)', (cn,))
            conn.commit()
    

        header = Label(main_frame, text="Courses", font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10)

        # Rectangle courses no. frame

        stats_frame = Frame(main_frame, bg=MAINFRAME_COLOR)
        stats_frame.pack()
        stat_box = Frame(stats_frame, bg=BUTTON_COLOR, width=120, height=60)
        stat_box.pack_propagate(False)
        stat_box.pack(side=LEFT, padx=10, pady=10)

        # How many courses
        c.execute('SELECT * FROM courses')
        courses = c.fetchall()
            
        stat_label = Label(stat_box, text=len(courses), font=("Arial", 14, "bold"), fg=FG_COLOR, bg=BUTTON_COLOR)
        stat_label.pack()
        stat_desc = Label(stat_box, text='Total Courses', font=("Arial", 10), fg=FG_COLOR, bg=BUTTON_COLOR)
        stat_desc.pack()

        # Search Frame
        search_frame = Frame(main_frame, bg=MAINFRAME_COLOR)
        search_frame.pack()

        search_entry = Entry(search_frame, font=("Arial", 10))
        search_entry.insert(0, 'Search...')  # Add the placeholder text
        search_entry.bind('<FocusIn>', on_entry_click)
        search_entry.bind('<FocusOut>', on_focusout)
        search_entry.config(fg='grey')
        search_entry.grid(row=0, column=0)

        search_btn = Button(search_frame, text='Search', command=search_courses)
        search_btn.grid(row=0, column=1, padx=10)

        # Table to display search results
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10)

        columns = ('course_id', 'coursename')
        table = ttk.Treeview(table_frame, columns=columns, show='headings')
        table.heading('course_id', text='Course ID')
        table.heading('coursename', text='Course Name')
        table.pack()

        # To display all courses at first
        update_table(courses)



    # Leaderboard - admin section
    elif btn_text == buttons[3]:
        pass

    # Mocktest - admin section - aayush
    elif btn_text == buttons[4]:


        #header section
        header = Label(main_frame, text="Mock Test", font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10)

               
                
                

                    
        
        

        def setup_database():
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()

            # Create mocktests table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mocktests (
                    mocktest_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mocktest_name TEXT NOT NULL,
                    fullmark INTEGER NOT NULL,
                    passmark INTEGER NOT NULL
                )
            ''')

            # Create courses table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_name TEXT NOT NULL
                )
            ''')

            # Create categories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_name TEXT NOT NULL
                )
            ''')

            # Create mockquestions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mockquestions (
                    mockquestion_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mocktest_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    category_id INTEGER NOT NULL,
                    no_of_questions INTEGER NOT NULL,
                    FOREIGN KEY (mocktest_id) REFERENCES mocktests (mocktest_id),
                    FOREIGN KEY (course_id) REFERENCES courses (course_id),
                    FOREIGN KEY (category_id) REFERENCES categories (category_id)
                )
            ''')

            conn.commit()
            conn.close()

        #takes data from mock table
        def fetch_mock_tests():
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mocktests")
            tests = cursor.fetchall()
            conn.close()
            return tests
        
        #takes data from mockquestions table
        def fetch_questions():
           conn = sqlite3.connect(DATABASE_FILE)
           cursor = conn.cursor()
           cursor.execute("SELECT * FROM mockquestions")
           questions = cursor.fetchall()
           conn.close()
           return questions
        
        #takes data from corses
        def fetch_courses():
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses")
            courses = cursor.fetchall()
            conn.close()
            return courses

       # Modify fetch_categories to filter by course_id
        def fetch_categories(course_id=None):
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            if course_id:
                cursor.execute("SELECT * FROM categories WHERE course_id = ?", (course_id,))
            else:
                cursor.execute("SELECT * FROM categories")
            categories = cursor.fetchall()
            conn.close()
            return categories
        
        def delete_question(question_id):
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mockquestions WHERE mockquestion_id = ?", (question_id,))
            conn.commit()
            conn.close()
            update_questions_table()


        def delete_selected_question():
            selected_item = questions_table.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a question to delete.")
                return
            question_id = questions_table.item(selected_item)["values"][0]
            delete_question(question_id)
            messagebox.showinfo("Success", "Question deleted successfully!")
                
        def delete_mock_test():
            selected_item = mock_test_table.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a mock test to delete.")
                return
            mock_test_id = mock_test_table.item(selected_item)["values"][0]
            
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mocktests WHERE mocktest_id = ?", (mock_test_id,))
            cursor.execute("DELETE FROM mockquestions WHERE mocktest_id = ?", (mock_test_id,))  # Delete related questions
            conn.commit()
            conn.close()
            update_mock_test_table()
            update_questions_table()
            messagebox.showinfo("Success", "Mock test deleted successfully!")

        #updates question table everytime we make changes
        def update_questions_table():
           for row in questions_table.get_children():
                questions_table.delete(row)
           for question in fetch_questions():
                mocktest_name = next((test[1] for test in fetch_mock_tests() if test[0] == question[1]), None)
                course_name = next((test[1] for test in fetch_courses() if test[0] == question[2]), None)
                questions_table.insert("", "end", values=(question[0], mocktest_name, course_name, question[3], question[4]))
        
        #Function to add mocktest name, full marks, passmarks
        def add_mock_test():
            add_mocktest = tk.Toplevel(main_frame)
            add_mocktest.title("Add Questions To Mock Test")
            add_mocktest.geometry("600x300")
            add_mocktest.attributes('-topmost', True)
    
            
           
            
            
            
            tk.Label(add_mocktest, text="Enter Mock Test Name:").pack()
            e1 = Entry(add_mocktest, width=35)
            e1.pack(pady=10)

            tk.Label(add_mocktest, text="Enter Mock Test description:").pack()
            text_desc = Text(add_mocktest,height=2, width=40)
            text_desc.pack(pady=10)
            
            tk.Label(add_mocktest, text="Enter Full Marks:").pack()
            e2 = Entry(add_mocktest, width=35)
            e2.pack(pady=10)
            tk.Label(add_mocktest, text="Enter Pass Marks:").pack()
            e3 = Entry(add_mocktest, width=35)
            e3.pack(pady=10)

            #saves the input taken from admin 
            def save_mock():
                mocktest_name = e1.get().strip()  # Get the value and strip whitespace
                mocktest_desc = text_desc.get("1.0", "end-1c")
                full_marks = e2.get().strip()      # Get the value and strip whitespace
                pass_marks = e3.get().strip()       # Get the value and strip whitespace
        
        # Check if any field is empty
                if not mocktest_name or not mocktest_desc or not full_marks or not pass_marks:
                   messagebox.showwarning("Warning", "Please fill in all fields.")
                   

                elif full_marks <= pass_marks:
                    messagebox.showwarning("Warning", "Passmarks should be less than fullmarks!")
                    

                else:
                    try:
                        conn = sqlite3.connect(DATABASE_FILE)
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO mocktests (mocktest_name, mocktest_desc, fullmark, passmark) VALUES (?,?,?,?)", 
                                    (mocktest_name,mocktest_desc,full_marks,pass_marks))
                        conn.commit()
                        conn.close()
                        update_mock_test_table()
                        messagebox.showinfo("Success", "Test added successfully!")
                        add_mocktest.destroy()
                    except sqlite3.IntegrityError:
                        messagebox.showerror("Error", "Mock test with this name already exists.")
                    
                    
            
            #tk.Button(add_mocktest, text="Save", command=save_mock).pack()

            add_mocktest.attributes('-toolwindow', True)

            def cancel():
                add_mocktest.destroy()

            btn_frame = Frame(add_mocktest )
            btn_frame.pack(pady = 10,fill=X,)
                
            update_btn=Button(btn_frame, text="Save", command=save_mock,font= button_font, fg= FG_COLOR ,bg = BUTTON_COLOR)
            update_btn.pack(side=LEFT,padx = 100)
            cancel_btn = Button(btn_frame, text="Cancel", command=cancel, bg = LOGOUT_COLOR,font = button_font,fg = FG_COLOR)
            cancel_btn.pack(side=RIGHT,padx = 100)
           
        
        #function to add questions to specific test, corse, category
        def add_mock_question():
            add_question_window = tk.Toplevel(main_frame)
            add_question_window.title("Add Questions To Mock Test")
            add_question_window.geometry("600x300")
            course_id = None
            category_id = None
            add_question_window.attributes('-topmost', True)
           

            tk.Label(add_question_window, text="Mock Test Name:").pack()
            test_names = [test[1] for test in fetch_mock_tests()]
            mock_test_combo = ttk.Combobox(add_question_window, values=test_names, state='readonly')
            mock_test_combo.pack()
            
            tk.Label(add_question_window, text="Courses:").pack()
            course_names = [test[1] for test in fetch_courses()]
            courses_combo = ttk.Combobox(add_question_window, values= course_names, state='readonly')
            courses_combo.pack()
            
            tk.Label(add_question_window, text="Categories:").pack()
            
            categories_combo = ttk.Combobox(add_question_window, state='readonly')
            categories_combo.pack()

              # Update categories based on selected course
            def update_categories(event):
                selected_course_name = courses_combo.get()
                course_id = next((course[0] for course in fetch_courses() if course[1] == selected_course_name), None)
                if course_id:
                    category_names = [category[1] for category in fetch_categories(course_id)]
                    categories_combo['values'] = category_names
                    categories_combo.set('')  # Clear the current selection

                
            def update_question(event):
                if categories_combo.get():
                    selected_course_name = courses_combo.get()
                    nonlocal course_id
                    nonlocal category_id
                    course_id = next((course[0] for course in fetch_courses() if course[1] == selected_course_name), None)


                    category = categories_combo.get()
                    category_id = next((cat[0] for cat in fetch_categories(course_id) if cat[1] == category), None)
                    no_of_question(course_id,category_id)

            def no_of_question(course_id,category_id):
                conn = sqlite3.connect(DATABASE_FILE)
                cursor = conn.cursor()
                cursor.execute("SELECT question_id FROM questions WHERE course_id=? AND category_id=?", (course_id,category_id,))
                question_no = cursor.fetchall()
                question_no = str(len(question_no))
                conn.commit()
                conn.close()
                check_qno.config(text=f'Total Questions in {categories_combo.get()} :: {question_no}')
                return question_no
                

            courses_combo.bind("<<ComboboxSelected>>", update_categories)  # Bind the event
            categories_combo.bind("<<ComboboxSelected>>", update_question)  # Bind the event

            check_qno =Label(add_question_window,text= '')
            check_qno.pack()
            
            tk.Label(add_question_window, text="No of Questions:").pack()
            questions_entry = tk.Entry(add_question_window)
            questions_entry.pack()


    
            def save_question():
                selected_test = mock_test_combo.get()
                course = courses_combo.get()
                category = categories_combo.get()
                num_questions = questions_entry.get()
                
                nonlocal course_id
                nonlocal category_id
                
                if not (selected_test and course and category and num_questions.isdigit()):
                    messagebox.showerror("Error", "Please fill all fields correctly.")
                    
              
                elif num_questions > no_of_question(course_id,category_id):
                    messagebox.showerror('Error', 'Please insert valid no of questions!')
                   
                else:

                
                    mock_test_id = next((test[0] for test in fetch_mock_tests() if test[1] == selected_test), None)
                    course_id = next((test[0] for test in fetch_courses() if test[1] == course), None)
                    category_id = next((cat[0] for cat in fetch_categories(course_id) if cat[1] == category), None)

                    # Debugging statements
                    print(f"Mock Test ID: {mock_test_id}, Course ID: {course_id}, Category ID: {category_id}, No of Questions: {num_questions}")

                    # Check if IDs are retrieved correctly
                    if not all([mock_test_id, course_id, category_id]):
                        messagebox.showerror("Error", "Could not find the selected IDs. Please check your selections.")
                        return

                    
                    conn = sqlite3.connect(DATABASE_FILE)
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO mockquestions (mocktest_id, course_id, category_id, no_of_questions) VALUES (?, ?, ?, ?)",
                                (mock_test_id, course_id, category_id,
                                num_questions))
                    conn.commit()
                    conn.close()
                    update_questions_table()
                    messagebox.showinfo("Success", "Question added successfully!")
                    add_question_window.destroy()
        
             #tk.Button(add_question_window, text="Save", command=save_question).pack()

            add_question_window.attributes('-toolwindow', True)

            def cancel():
                add_question_window.destroy()

            btn_frame = Frame(add_question_window )
            btn_frame.pack(pady = 10,fill=X,)
            
            update_btn=Button(btn_frame, text="Save", command=save_question,font= button_font, fg= FG_COLOR ,bg = BUTTON_COLOR)
            update_btn.pack(side=LEFT,padx = 100)
            cancel_btn = Button(btn_frame, text="Cancel", command=cancel, bg = LOGOUT_COLOR,font = button_font,fg = FG_COLOR)
            cancel_btn.pack(side=RIGHT,padx = 100)
        

        # Updates the mock test table with every change
        def update_mock_test_table():
            for row in mock_test_table.get_children():
                mock_test_table.delete(row)
            for test in fetch_mock_tests():
                mock_test_table.insert("", "end", values=(test[0], test[1], test[2], test[3],test[4]))

       
        setup_database()
        
        #main frame for table
        mocktable_frame = Frame(main_frame,bg = MAINFRAME_COLOR)
        mocktable_frame.pack(pady=10)

        mocktest_frame = Frame(mocktable_frame,bg = MAINFRAME_COLOR)
        mocktest_frame.pack(fill = X,pady = 10)

        add_test_btn = Button(mocktest_frame, text="Add Mock Test", command=add_mock_test, bg= BUTTON_COLOR, font= button_font , fg= FG_COLOR )
        add_test_btn.pack(side=LEFT, pady=10)

        delete_btn = Button(mocktest_frame, text="Delete Mock Test", command=delete_mock_test, bg= LOGOUT_COLOR, font= button_font, fg= FG_COLOR  )
        delete_btn.pack(side=RIGHT, pady=10)
        



        # Create UI elements
        list_mocktest = ["ID", "Mock Test Name","Mocktest Description", "Full Mark", "Pass Mark"]
        mock_test_table = ttk.Treeview(mocktable_frame, columns=list_mocktest, show="headings")
        for i in list_mocktest:

            mock_test_table.heading(i, text=i)
            mock_test_table.column(i,anchor= CENTER)
        # mock_test_table.heading("Mock Test Name", text="Mock Test Name")
        # mock_test_table.heading("Mocktest Description", text="Mocktest Description")
        # mock_test_table.heading("Full Mark", text="Full Mark")
        # mock_test_table.heading("Pass Mark", text="Pass Mark")
        mock_test_table.pack(fill=BOTH, expand=True)

        # Buttons to add mock tests and mock questions
        btn_frame = Frame(mocktable_frame, bg = MAINFRAME_COLOR)
        btn_frame.pack(fill = X,pady=10)

        
        add_question_btn = Button(btn_frame, text="Add No Of Questions", command=add_mock_question, bg= BUTTON_COLOR, font= button_font, fg= FG_COLOR  )
        add_question_btn.pack(side=LEFT, pady=10)

        delete_btn = Button(btn_frame, text="Delete Mock QNs", command=delete_selected_question, bg= LOGOUT_COLOR, font= button_font, fg= FG_COLOR  )
        delete_btn.pack(side=RIGHT, pady=10)
        

      

        #question table
        
        questions_table = ttk.Treeview(main_frame, columns=("ID", "Mock Test-Name", "Course-Name", "Category", "Questions"), show="headings")
        for col in ["ID", "Mock Test-Name", "Course-Name", "Category", "Questions"]:
               questions_table.heading(col, text=col)
               questions_table.column(col,anchor=CENTER)
        questions_table.pack()

       


        update_mock_test_table()
        update_questions_table()
       



    # Question - admin section
    elif btn_text == buttons[5]:

        
        #header section
        header = Label(main_frame, text="Questions", font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10)



        def fetch_questions():
           conn = sqlite3.connect(DATABASE_FILE)
           cursor = conn.cursor()
           cursor.execute("SELECT * FROM questions")
           questions = cursor.fetchall()
           conn.close()
           return questions
        

        #takes data from corses
        def fetch_courses():
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses")
            courses = cursor.fetchall()
            conn.close()
            return courses

       # Modify fetch_categories to filter by course_id
        def fetch_categories(course_id=None):
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            if course_id:
                cursor.execute("SELECT * FROM categories WHERE course_id = ?", (course_id,))
            else:
                cursor.execute("SELECT * FROM categories")
            categories = cursor.fetchall()
            conn.close()
            return categories
        
        #Search function
        def search_questions():
            query = search_entry.get().strip().lower()
            for row in questions_table.get_children():
                questions_table.delete(row)

            i = 0
            for question in fetch_questions():
                course_name = next((test[1] for test in fetch_courses() if test[0] == question[1]), None)
                category_name = next((test[1] for test in fetch_categories() if test[0] == question[2]), None)

                try:
                    options = json.loads(question[5])  # Load JSON
                    if isinstance(options, list):
                        options = ", ".join(options)
                    else:
                        options = str(options)
                except json.JSONDecodeError:
                    options = "Invalid data"

                # Check if query matches any field
                if (query in question[3].lower() or query in options.lower() or 
                    query in str(course_name).lower() or query in str(category_name).lower()):
                    questions_table.insert("", "end", values=(question[0], question[3], question[4], options, course_name, category_name))
                    i += 1
            total.config(text=f'{i}')

        # Add a frame for the search bar
        search_frame = Frame(main_frame, bg=MAINFRAME_COLOR)
        search_frame.pack(pady=10, fill=X)

        # Add a search entry box
        search_entry = Entry(search_frame, width=30,font=(15))
        search_entry.pack(side=LEFT, padx=10, pady=5)

        # Add a search button
        search_button = Button(search_frame, text="Search", command=search_questions, bg=BUTTON_COLOR, font=button_font, fg=FG_COLOR)
        search_button.pack(side=LEFT, padx=5)

        
        #Update question table
        def update_questions_table():
            for row in questions_table.get_children():
                questions_table.delete(row)
           
            i = 0
            for question in fetch_questions():
               
                course_name = next((test[1] for test in fetch_courses() if test[0] == question[1]), None)
                category_name = next((test[1] for test in fetch_categories() if test[0] == question[2]), None)
                 # Ensure the data is properly converted into a list
                try:
                    options = json.loads(question[5])  # Load JSON
                    if isinstance(options, list):  # Check if it's a list
                        options = ", ".join(options)  # Convert list to a string (for display)
                    else:
                        options = str(options)  # Convert to string if it's not a list
                except json.JSONDecodeError:
                    options = "Invalid data"  # Handle error if JSON is malformed
                
                i += 1
                #Insert into Treeview
                questions_table.insert("", "end", values=(question[0], question[3], question[4], options, course_name, category_name))
            total.config(text=f'{i}')
        
        
        #Delete question table
        def delete_question_selected():
            selected_item = questions_table.selection()
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select a question to edit.")
                return

            selected_question = questions_table.item(selected_item, "values")
            print(selected_question[0])
            option = messagebox.askokcancel('Delete records',f'Do you want to delete Q:{selected_question[1]}')
            if option :


                conn= sqlite3.connect(DATABASE_FILE)
                cursor= conn.cursor()
                cursor.execute('DELETE FROM questions WHERE question_id= ? ', (selected_question[0],))
                conn.commit()
                conn.close()
                update_questions_table()
        
        def open_add_question_form():
            add_window = tk.Toplevel(main_frame)
            add_window.title("Add Question")
            add_window.geometry("600x450")

            #Courses
            tk.Label(add_window, text="Courses:").pack()
            course_names = [test[1] for test in fetch_courses()]
            courses_combo = ttk.Combobox(add_window, values= course_names, state='readonly')
            courses_combo.pack(pady=10)

            #Category   
            tk.Label(add_window, text="Categories:").pack()
             
            categories_combo = ttk.Combobox(add_window,state='readonly')
            categories_combo.pack(pady=10)

              # Update categories based on selected course
            def update_categories(event):
                selected_course_name = courses_combo.get()
                course_id = next((course[0] for course in fetch_courses() if course[1] == selected_course_name), None)
                if course_id:
                    category_names = [category[1] for category in fetch_categories(course_id)]
                    categories_combo['values'] = category_names
                    categories_combo.set('')  # Clear the current selection

            courses_combo.bind("<<ComboboxSelected>>", update_categories)  # Bind the event

            #Question
            tk.Label(add_window,text='Enter question:').pack()
            #question_box = Entry(add_window, width=35)
            #question_box.pack()
            question_box= Text(add_window,height= 5,width= 40)
            question_box.pack(pady=10)
            
            tk.Label(add_window, text="Incorrect answer:").pack()
            #Incorrect_box = Entry(add_window, width=35)
            #Incorrect_box.pack()
            Incorrect_box = Text(add_window, height= 2, width = 40)
            Incorrect_box.pack(pady=10)

            tk.Label(add_window, text="Correct answer:").pack()
            correct_box = Text(add_window, height=1, width=40)
            correct_box.pack(pady=10)

            def save_question():
                
                course = courses_combo.get()
                category = categories_combo.get()
                Question = question_box.get("1.0", "end-1c")  # Get the value and strip whitespace
                Incorrect_ans = f"{Incorrect_box.get("1.0", "end-1c")}"
                Incorrect_ans = json.dumps(Incorrect_ans.split(','))
                # print(Incorrect_ans.split(','))
                # Get the value and strip whitespace
                Correct_ans = correct_box.get("1.0", "end-1c")      # Get the value and strip whitespace
                
                
                if not ( course or category or Question or Incorrect_ans or Correct_ans):
                    messagebox.showerror("Error", "Please fill all fields correctly.")
                    return
                
                
                course_id = next((test[0] for test in fetch_courses() if test[1] == course), None)
                category_id = next((cat[0] for cat in fetch_categories(course_id) if cat[1] == category), None)

                 # Debugging statements
                print(f" Course ID: {course_id}, Category ID: {category_id}")

                # Check if IDs are retrieved correctly
                if not all([ course_id, category_id]):
                    messagebox.showerror("Error", "Could not find the selected IDs. Please check your selections.")
                    return

                
                conn = sqlite3.connect(DATABASE_FILE)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO questions ( question,course_id, category_id, correct_ans, incorrect_ans) VALUES (?,?, ?, ?, ?)",
                            ( Question,course_id, category_id, Correct_ans,Incorrect_ans
                              ))
                conn.commit()
                conn.close()
                update_questions_table()
                
                messagebox.showinfo("Success", "Question added successfully!")
                add_window.destroy()
                
        
            #tk.Button(add_window, text="Save", command=save_question).pack()

            add_window.attributes('-toolwindow', True)

            def cancel():
                add_window.destroy()

            btn_frame = Frame(add_window, )
            btn_frame.pack(pady = 10,fill=X,)
                
            update_btn=Button(btn_frame, text="Save", command=save_question,font= button_font, fg= FG_COLOR ,bg = BUTTON_COLOR)
            update_btn.pack(side=LEFT,padx = 100)
            cancel_btn = Button(btn_frame, text="Cancel", command=cancel, bg = LOGOUT_COLOR,font = button_font,fg = FG_COLOR)
            cancel_btn.pack(side=RIGHT,padx = 100)
           

        #Edit question form
        def open_edit_question_form():
            selected_item = questions_table.selection()
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select a question to edit.")
                return

            selected_question = questions_table.item(selected_item, "values")
            
           
            edit_window = tk.Toplevel(main_frame)
            edit_window.title("Edit Question")
            edit_window.geometry("600x450")

            #Courses
            tk.Label(edit_window, text="Courses:").pack()

            # Fetch courses and set default selection
            course_names = [course[1] for course in fetch_courses()]
            c_name = tk.StringVar()
            c_name.set(selected_question[4])  # Default selection

            # Create Course ComboBox
            courses_combo = ttk.Combobox(edit_window, textvariable=c_name, values=course_names, state="readonly")
            courses_combo.pack(pady=10)

            # Label for Categories
            tk.Label(edit_window, text="Categories:").pack()

            # Fetch initial categories based on the default course
            default_course_id = next((course[0] for course in fetch_courses() if course[1] == c_name.get()), None)
            category_names = [category[1] for category in fetch_categories(default_course_id)]

            # Create Category ComboBox
            ca_name = tk.StringVar()
            ca_name.set(selected_question[5])  # Default selection

            categories_combo = ttk.Combobox(edit_window, textvariable=ca_name, values=category_names, state="readonly")
            categories_combo.pack(pady=10)

            # Function to update categories when a course is selected
            def update_categories(event):
                selected_course_name = c_name.get()
                selected_course_id = next((course[0] for course in fetch_courses() if course[1] == selected_course_name), None)
                
                if selected_course_id is not None:
                    new_category_names = [category[1] for category in fetch_categories(selected_course_id)]
                    categories_combo['values'] = new_category_names  # Update category dropdown
                    if new_category_names:
                        ca_name.set(new_category_names[0])  # Set first category as default
                    else:
                        ca_name.set("")  # Clear selection if no categories available

            # Bind course selection to update categories
            courses_combo.bind("<<ComboboxSelected>>", update_categories)

            #Question
            tk.Label(edit_window,text='Enter question:').pack()
            question_box = Text(edit_window, height=5,width=40)
            question_box.insert('1.0',selected_question[1])
            question_box.pack(pady = 10)

            tk.Label(edit_window, text="Incorrect answer:").pack()
            Incorrect_box = Text(edit_window,height=2, width=40)
            Incorrect_box.insert('1.0',selected_question[3])
            Incorrect_box.pack(pady=10)

            tk.Label(edit_window, text="Correct answer:").pack()
            correct_box = Text(edit_window,height=1, width=40)
            correct_box.insert('1.0',selected_question[2])
            correct_box.pack(pady=10)

            def save_question():
                course = c_name.get()
                category = ca_name.get()
                Question = question_box.get("1.0", "end-1c")  # Get the value and strip whitespace
                Incorrect_ans = f"{Incorrect_box.get("1.0", "end-1c")}"
                Incorrect_ans = json.dumps(Incorrect_ans.split(','))
                Correct_ans = correct_box.get("1.0", "end-1c") # Get the value and strip whitespace

                if not (course and category and Question and Incorrect_ans and Correct_ans):
                    messagebox.showerror("Error", "Please fill all fields correctly.")
                    return

                course_id = next((test[0] for test in fetch_courses() if test[1] == course), None)
                category_id = next((cat[0] for cat in fetch_categories(course_id) if cat[1] == category), None)

                # Retrieve the question ID from the selected question
                question_id = selected_question[0]  # Assuming the question ID is the first element in selected_question

                # Debugging statements
                print(f"Course ID: {course_id}, Category ID: {category_id}, Question ID: {question_id}")

                # Check if IDs are retrieved correctly
                if not all([course_id, category_id, question_id]):
                    messagebox.showerror("Error", "Could not find the selected IDs. Please check your selections.")
                    return

                conn = sqlite3.connect(DATABASE_FILE)
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE questions SET question=?, course_id=?, category_id=?, correct_ans=?, incorrect_ans=? WHERE question_id=?",
                    (Question, course_id, category_id, Correct_ans, Incorrect_ans, question_id)
                )
                conn.commit()
                conn.close()
                update_questions_table()

                messagebox.showinfo("Success", "Question edited successfully!")
                edit_window.destroy()
            
            edit_window.attributes('-toolwindow', True)

            def cancel():
                edit_window.destroy()

            btn_frame = Frame(edit_window, )
            btn_frame.pack(pady = 10,fill=X,)
                
            update_btn=Button(btn_frame, text="Update", command=save_question,font= button_font, fg= FG_COLOR ,bg = BUTTON_COLOR)
            update_btn.pack(side=LEFT,padx = 100)
            cancel_btn = Button(btn_frame, text="Cancel", command=cancel, bg = LOGOUT_COLOR,font = button_font,fg = FG_COLOR)
            cancel_btn.pack(side=RIGHT,padx = 100)
           

                
                



       


        questiontable_frame = Frame(main_frame, bg = MAINFRAME_COLOR, height = 50, width = 90)
        questiontable_frame.pack(pady=10,fill=BOTH,expand=  True)

        addquestion_btn = Button(search_frame, text="Add Question", command=open_add_question_form, bg= BUTTON_COLOR, font= button_font, fg= FG_COLOR  )
        addquestion_btn.pack(side=RIGHT, padx=10,pady = 10)



        questions_table = ttk.Treeview(questiontable_frame, columns=("Id", "Question", "Correct","Incorrect",  "Courses", "Category"), show="headings")

        # Define column headings
        questions_table.heading("Id", text="Id")
        questions_table.heading("Question", text="Question")
        questions_table.heading("Incorrect", text="Incorrect")  # Fixed capitalization
        questions_table.heading("Correct", text="Correct")
        questions_table.heading("Courses", text="Courses")  # Ensure consistency
        questions_table.heading("Category", text="Category")

        # Adjust column widths
        questions_table.column("Id", width=50, anchor=CENTER)
        questions_table.column("Question", width=250,anchor=CENTER)
        questions_table.column("Incorrect", width=100, anchor=CENTER)
        questions_table.column("Correct", width=100, anchor=CENTER)
        questions_table.column("Courses", width=150,anchor=CENTER)
        questions_table.column("Category", width=150,anchor=CENTER)

        # Pack the Treeview
        questions_table.pack(fill=BOTH, expand=True,padx = 10, pady = 10)


        
        editquestion_btn = Button(questiontable_frame, text="Edit Question", command=open_edit_question_form, bg= BUTTON_COLOR, font= button_font, fg= FG_COLOR  )
        editquestion_btn.pack(side=LEFT, padx=10,pady = 10)

        del_question_btn = Button(questiontable_frame, text="Delete Question", command=delete_question_selected, bg= LOGOUT_COLOR, font= button_font, fg= FG_COLOR  )
        del_question_btn.pack(side=LEFT, padx=10,pady = 10)

        total_frame = Frame(questiontable_frame)
        total_frame.pack(side=RIGHT)

        total= Label(total_frame,text='',font = button_font)
        total.pack(side=RIGHT,padx=100)

        total_label= Label(total_frame,text='Total Questions : ',font = button_font)
        total_label.pack(side=RIGHT)




        update_questions_table()





    else:
        label = Label(main_frame, text=btn_text, font=("Arial", 20, "bold"), bg=MAINFRAME_COLOR)
        label.pack(expand=True)

# Sidebar
sidebar = Frame(root, bg=SIDEBAR_COLOR, width=200, height=600)
sidebar.pack(side=LEFT, fill=Y)

profile_frame = Frame(sidebar, bg=SIDEBAR_COLOR)
profile_frame.pack(pady=20)

profile_icon = Label(profile_frame, text="🧑", font=("Arial", 40), bg=SIDEBAR_COLOR, fg=FG_COLOR)
profile_icon.pack()

profile_name = Label(profile_frame, text="Admin", font=label_font, bg=SIDEBAR_COLOR, fg=FG_COLOR)
profile_name.pack()



# Sidebar buttons
buttons = ["Dashboard", "Users", "Courses", "LeaderBoard", "Mock Test", "Questions"]
for btn_text in buttons:
    sidebarbutton = Button(sidebar, text=btn_text, bg=BUTTON_COLOR, fg=FG_COLOR, relief=FLAT, width=20, height=2, command=lambda bt=btn_text: openbutton(bt))
    sidebarbutton.pack(pady=2)
    buttons_dict[btn_text] = sidebarbutton

logout_btn = Button(sidebar, text="🔓 LogOut", bg=LOGOUT_COLOR, fg=FG_COLOR, relief=FLAT, width=20, height=2)
logout_btn.pack(pady=20)

# Main Dashboard
main_frame = Frame(root, bg=MAINFRAME_COLOR)
main_frame.pack(expand=True, fill=BOTH)

# Initialize with Dashboard
openbutton(buttons[0])

root.mainloop()
