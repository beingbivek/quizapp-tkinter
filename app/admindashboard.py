from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
from PIL import ImageTk, Image
import runpy
import sqlite3
from tkinter import simpledialog
import tkinter as tk

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

    # Main Dashboard - bivek
    if btn_text == buttons[0]:
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

        # Courses Functions

        def on_entry_click(event):
            # Function to remove placeholder text when the entry is clicked.
            if search_course_entry.get() == 'Search...':
                search_course_entry.delete(0, "end")  # delete all the text in the entry
                search_course_entry.insert(0, '')  # Insert blank for user input
                search_course_entry.config(fg='black')

        def on_focusout(event):
            # Function to add placeholder text if the entry is empty when focus is lost.
            if search_course_entry.get() == '':
                search_course_entry.insert(0, 'Search...')
                search_course_entry.config(fg='grey')
                # display all courses after the search bar is empty
                update_course_table(get_courses())

        def search_courses():
            query = f'SELECT * FROM courses WHERE coursename LIKE ?'
            # query = f'SELECT * FROM courses'
            search_term = f'%{search_course_entry.get()}%'
            # c.execute(query)
            c.execute(query, (search_term,))
            results = c.fetchall()
            # print(results)
            
            # show the search result
            update_course_table(results)

        def update_course_table(results):
            for row in course_table.get_children():
                course_table.delete(row)
            for row in results:
                course_table.insert('', 'end', values=row)


        def add_course():

            def save_course():
                try:
                    all_courses = get_courses()
                    for course in all_courses:
                        if course[1].lower() == course_name_entry.get().lower():
                            messagebox.showerror(title='Course Name Repeated',message='Course Name is being repeated so use another name.')
                            add_course()
                            break
                    else:
                        c.execute('INSERT INTO courses (coursename) VALUES (?)', (course_name_entry.get(),))
                        conn.commit()
                        update_course_table(get_courses())
                        messagebox.showinfo(title='Success',message='Course successfully created.')
                except Exception as e:
                    print(e)

            def cancel_course():
                add_course_window.destroy()

            add_course_window = Toplevel(main_frame)
            add_course_window.title('Add Course')
            add_course_window.geometry('400x300')

            add_course_window.resizable(False, False)  # Prevent window resizing
            add_course_window.wm_attributes("-toolwindow", 1) # Disable max and min button

            add_course_frame = Frame(add_course_window,padx=10,pady=10,border=2,borderwidth=2)
            add_course_frame.pack()
            
            # Frame for the first row
            row1 = Frame(add_course_window, padx=10, pady=10, border=2, borderwidth=2)
            row1.pack(fill='x')

            course_name_label = Label(row1, text='Course Name', font=("Arial", 14))
            course_name_label.pack(side='left', pady=5, padx=5)

            course_name_entry = Entry(row1, font=("Arial", 12))
            course_name_entry.pack(side='right', padx=5)

            # Frame for the second row
            row2 = Frame(add_course_window, padx=10, pady=10, border=2, borderwidth=2)
            row2.pack(fill='x')

            save_course_btn = Button(row2, text='Save', command=save_course, font=("Arial", 12), fg='white', bg='blue')
            save_course_btn.pack(side='left', padx=5, pady=5)

            close_course_btn = Button(row2, text='Cancel', command=cancel_course, font=("Arial", 12), fg='white', bg='red')
            close_course_btn.pack(side='right', padx=5, pady=5)


        # Database Connection
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()

        # demo courses creation or insertion
        # c.execute('SELECT * FROM courses')
        # cou = c.fetchall()
        # if not cou:
        #     for cn in defcourses:
        #         c.execute('INSERT INTO courses (coursename) VALUES (?)', (cn,))
        #     conn.commit()
    

        header = Label(main_frame, text="Courses", font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10)

        # Courses Section

        # Rectangle courses no. frame

        stats_frame = Frame(main_frame, bg=MAINFRAME_COLOR)
        stats_frame.pack()
        stat_box = Frame(stats_frame, bg=BUTTON_COLOR, width=120, height=60)
        stat_box.pack_propagate(False)
        stat_box.pack(side=LEFT, padx=10, pady=10)

        # How many courses
        def get_courses():
            c.execute('SELECT * FROM courses')
            return c.fetchall()
            
        stat_label = Label(stat_box, text=len(get_courses()), font=("Arial", 14, "bold"), fg=FG_COLOR, bg=BUTTON_COLOR)
        stat_label.pack()
        stat_desc = Label(stat_box, text='Total Courses', font=("Arial", 10), fg=FG_COLOR, bg=BUTTON_COLOR)
        stat_desc.pack()

        # Search Frame for courses
        course_frame = Frame(main_frame, bg=MAINFRAME_COLOR)
        course_frame.pack()

        search_course_frame = Frame(course_frame,bg=MAINFRAME_COLOR)

        search_course_entry = Entry(search_course_frame, font=button_font)
        search_course_entry.insert(0, 'Search...')  # Add the placeholder text
        search_course_entry.bind('<FocusIn>', on_entry_click)
        search_course_entry.bind('<FocusOut>', on_focusout)
        search_course_entry.config(fg='grey')
        search_course_entry.pack(side='left')

        search_course_btn = Button(search_course_frame, text='Search', command=search_courses, bg= BUTTON_COLOR, fg=FG_COLOR,font=button_font)
        search_course_btn.pack(side='right',padx=10)

        search_course_frame.pack(side='left',padx=screen_width/6)

        add_course_btn = Button(course_frame, text='Add Course', bg=BUTTON_COLOR, fg=FG_COLOR, font=button_font, command=add_course)
        add_course_btn.pack(side='right',padx=screen_width/6)

        # Table to display search results for courses
        course_table_frame = Frame(main_frame)
        course_table_frame.pack(pady=10)

        columns = ('course_id', 'coursename','actions')
        course_table = ttk.Treeview(course_table_frame, columns=columns, show='headings')
        course_table.heading('course_id', text='Course ID')
        course_table.heading('coursename', text='Course Name')
        course_table.heading('actions', text='Actions')
        course_table.pack()

        # To display all courses at first
        update_course_table(get_courses())


        # Categories section

        # Categories Functions

        def add_category():

            def save_category():
                try:
                    all_courses = get_courses()
                    for course in all_courses:
                        if course[1].lower() == course_name_entry.get().lower():
                            messagebox.showerror(title='Course Name Repeated',message='Course Name is being repeated so use another name.')
                            add_course()
                            break
                    else:
                        c.execute('INSERT INTO courses (coursename) VALUES (?)', (course_name_entry.get(),))
                        conn.commit()
                        update_course_table(get_courses())
                        messagebox.showinfo(title='Success',message='Course successfully created.')
                except Exception as e:
                    print(e)

            def cancel_category():
                add_category_window.destroy()

            add_category_window = Toplevel(main_frame)
            add_category_window.title('Add Course')
            add_category_window.geometry('400x300')

            add_category_window.resizable(False, False)  # Prevent window resizing
            add_category_window.wm_attributes("-toolwindow", 1) # Disable max and min button

            add_course_frame = Frame(add_category_window,padx=10,pady=10,border=2,borderwidth=2)
            add_course_frame.pack()
            
            # Frame for the first row
            row1 = Frame(add_category_window, padx=10, pady=10, border=2, borderwidth=2)
            row1.pack(fill='x')

            course_name_label = Label(row1, text='Course Name', font=("Arial", 14))
            course_name_label.pack(side='left', pady=5, padx=5)

            course_name_entry = Entry(row1, font=("Arial", 12))
            course_name_entry.pack(side='right', padx=5)

            # Frame for the second row
            row2 = Frame(add_category_window, padx=10, pady=10, border=2, borderwidth=2)
            row2.pack(fill='x')

            save_course_btn = Button(row2, text='Save', command=save_category, font=("Arial", 12), fg='white', bg='blue')
            save_course_btn.pack(side='left', padx=5, pady=5)

            close_course_btn = Button(row2, text='Cancel', command=cancel_category, font=("Arial", 12), fg='white', bg='red')
            close_course_btn.pack(side='right', padx=5, pady=5)

        def update_category_table(results):
            for row in category_table.get_children():
                category_table.delete(row)
            for row in results:
                category_table.insert('', 'end', values=row)

        # All categories data with coursename
        def get_categories():
            c.execute('SELECT * FROM categories')
            categories = c.fetchall()
            courses = get_courses()

            for category in categories:
                for course in courses:
                    if str(category[2]) == str(course[0]):
                        category[2] = course[1]
                        break
            
            # print(categories)

            return categories

        # Search Frame for courses
        category_frame = Frame(main_frame, bg=MAINFRAME_COLOR)
        category_frame.pack()

        search_category_frame = Frame(category_frame,bg=MAINFRAME_COLOR)
        search_category_frame.pack(side='left',padx=screen_width/6)

        search_category_entry = Entry(search_category_frame, font=button_font)
        search_category_entry.insert(0, 'Search...')  # Add the placeholder text
        search_category_entry.bind('<FocusIn>', on_entry_click)
        search_category_entry.bind('<FocusOut>', on_focusout)
        search_category_entry.config(fg='grey')
        search_category_entry.pack(side='left')

        search_category_btn = Button(search_category_frame, text='Search', command=search_courses, bg= BUTTON_COLOR, fg=FG_COLOR,font=button_font)
        search_category_btn.pack(side='right',padx=10)

        add_category_btn = Button(category_frame, text='Add Category', bg=BUTTON_COLOR, fg=FG_COLOR, font=button_font, command=add_category)
        add_category_btn.pack(side='right',padx=screen_width/6)

        # Table to display search results for courses
        category_table_frame = Frame(main_frame)
        category_table_frame.pack(pady=10)

        columns = ('category_id', 'categoryname','coursename','actions')
        category_table = ttk.Treeview(category_table_frame, columns=columns, show='headings')
        category_table.heading('category_id', text='Category ID')
        category_table.heading('categoryname', text='Category Name')
        category_table.heading('coursename', text='Course Name')
        category_table.heading('actions', text='Actions')
        category_table.pack()

        # To display all courses at first
        update_category_table(get_categories())

        # Close DB Connection
        conn.commit()
        conn.close()



    # Leaderboard - admin section
    elif btn_text == buttons[3]:
        pass

    # Mocktest - admin section - aayush
    elif btn_text == buttons[4]:


        #header section
        header = Label(main_frame, text="Mock Test", font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10)

               
                
                

                    
        
        

        def setup_database():
            conn = sqlite3.connect("quiz.db")
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

        def fetch_mock_tests():
            conn = sqlite3.connect("quiz.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mocktests")
            tests = cursor.fetchall()
            conn.close()
            return tests

        def fetch_courses():
            conn = sqlite3.connect("quiz.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses")
            courses = cursor.fetchall()
            conn.close()
            return courses

        def fetch_categories():
            conn = sqlite3.connect("quiz.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories")
            categories = cursor.fetchall()
            conn.close()
            return categories

        def add_mock_test():
            mock_test_name = simpledialog.askstring("Add Mock Test", "Enter Mock Test Name:")
            fullmark = simpledialog.askinteger("Add Mock Test", "Enter Full Marks:")
            passmark = simpledialog.askinteger("Add Mock Test", "Enter Pass Marks:")
            
            if not mock_test_name or fullmark is None or passmark is None:
                return
            
            try:
                conn = sqlite3.connect("quiz.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO mocktests (mocktest_name, fullmark, passmark) VALUES (?, ?, ?)", 
                            (mock_test_name, fullmark, passmark))
                conn.commit()
                conn.close()
                update_mock_test_table()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Mock test with this name already exists.")

        def add_mock_question():
            mock_test_id = simpledialog.askinteger("Add Mock Question", "Enter Mock Test ID:")
            course_id = simpledialog.askinteger("Add Mock Question", "Enter Course ID:")
            category_id = simpledialog.askinteger("Add Mock Question", "Enter Category ID:")
            no_of_questions = simpledialog.askinteger("Add Mock Question", "Enter Number of Questions:")
            
            if mock_test_id is None or course_id is None or category_id is None or no_of_questions is None:
                return
            
            try:
                conn = sqlite3.connect("quiz.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO mockquestions (mocktest_id, course_id, category_id, no_of_questions) VALUES (?, ?, ?, ?)", 
                            (mock_test_id, course_id, category_id, no_of_questions))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Mock question added successfully.")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Invalid Mock Test, Course, or Category ID.")

        def update_mock_test_table():
            for row in mock_test_table.get_children():
                mock_test_table.delete(row)
            for test in fetch_mock_tests():
                mock_test_table.insert("", "end", values=(test[0], test[1], test[2], test[3]))

       
        setup_database()

        mocktable_frame = Frame(main_frame)
        mocktable_frame.pack(pady=10)


        # Create UI elements
        mock_test_table = ttk.Treeview(mocktable_frame, columns=("ID", "Mock Test Name", "Full Mark", "Pass Mark"), show="headings")
        mock_test_table.heading("ID", text="ID")
        mock_test_table.heading("Mock Test Name", text="Mock Test Name")
        mock_test_table.heading("Full Mark", text="Full Mark")
        mock_test_table.heading("Pass Mark", text="Pass Mark")
        mock_test_table.pack(fill=BOTH, expand=True)

        # Buttons to add mock tests and mock questions
        btn_frame = Frame(main_frame, bg = MAINFRAME_COLOR)
        btn_frame.pack(pady=10)

        add_test_btn = Button(btn_frame, text="Add Mock Test", command=add_mock_test, bg= BUTTON_COLOR, font= button_font , fg= FG_COLOR )
        add_test_btn.pack(side=LEFT, padx=10)

        add_question_btn = Button(btn_frame, text="Add Mock Question", command=add_mock_question, bg= BUTTON_COLOR, font= button_font, fg= FG_COLOR  )
        add_question_btn.pack(side=LEFT, padx=10)

        update_mock_test_table()
       



    # Question - admin section
    elif btn_text == buttons[5]:
        pass

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
