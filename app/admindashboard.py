from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
from PIL import ImageTk, Image
import runpy
import sqlite3
from tkinter import simpledialog
import json
from tkcalendar import DateEntry  # Import DateEntry for date selection
from datetime import datetime, date

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
minclose_windowbtn(root)

def get_courses():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM courses')
    courses = c.fetchall()
    conn.close()
    return courses

# Store button references
buttons_dict = {}

# Functions
# How many courses
def get_courses():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM courses')
    courses = c.fetchall()
    conn.close()
    return courses

# Modify get_categories to filter by course_id
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

def stats():
    # Data from all tables
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM sqlite_sequence')
    stat_data = c.fetchall()
    conn.commit()
    conn.close()
    return stat_data

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

        stat_data = stats()

        # Show Stat Data
        for stat in stat_data:
            stat_box = Frame(stats_frame, bg=BUTTON_COLOR, width=150, height=60)
            stat_box.pack_propagate(False)
            stat_box.pack(side=LEFT, padx=10, pady=10)
            
            stat_label = Label(stat_box, text=stat[1], font=("Arial", 14, "bold"), fg=FG_COLOR, bg=BUTTON_COLOR)
            stat_label.pack()
            stat_desc = Label(stat_box, text=stat[0].upper(), font=("Arial", 10), fg=FG_COLOR, bg=BUTTON_COLOR)
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

        # Function to fetch users from the database
        def fetch_users():
            try:
                conn = sqlite3.connect(DATABASE_FILE)
                c = conn.cursor()
                c.execute("SELECT user_id, username, fullname, contact, email, address FROM users")
                users = c.fetchall()
                conn.close()
                return users
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while fetching users: {e}")
                return []

        # Function to refresh the table with data from the database
        def refresh_table():
            global rows
            rows = fetch_users()  # Fetch users from the database
            for row in tree.get_children():
                tree.delete(row)  # Clear the existing rows in the table
            for row in rows:
                tree.insert("", "end", values=row)  # Insert fetched data into the table

        # Function to handle user registration
        def register_user():
            register_window = Toplevel(main_frame)
            register_window.title("Register User")
            register_window.geometry("500x400")

            # Labels and Entries
            Label(register_window, text="Username:").pack()
            username_entry = Entry(register_window)
            username_entry.pack()

            Label(register_window, text="Full Name:").pack()
            fullname_entry = Entry(register_window)
            fullname_entry.pack()

            Label(register_window, text="Contact:").pack()
            contact_entry = Entry(register_window)
            contact_entry.pack()

            Label(register_window, text="Email:").pack()
            email_entry = Entry(register_window)
            email_entry.pack()

            Label(register_window, text="Address:").pack()
            address_entry = Entry(register_window)
            address_entry.pack()

            Label(register_window, text="Password:").pack()
            password_entry = Entry(register_window, show="*")
            password_entry.pack()

            Label(register_window, text="Security Question:").pack()
            sq_var = StringVar(value=security_questions[0])
            OptionMenu(register_window, sq_var, *security_questions).pack()

            Label(register_window, text="Security Answer:").pack()
            sq_answer_entry = Entry(register_window)
            sq_answer_entry.pack()

            # Submit Button
            Button(register_window, text="Submit", command=lambda: submit_registration(
                username_entry.get(),
                fullname_entry.get(),
                contact_entry.get(),
                email_entry.get(),
                address_entry.get(),
                password_entry.get(),
                sq_var.get(),
                sq_answer_entry.get(),
                register_window
            )).pack()

        # Function to submit user registration
        def submit_registration(username, fullname, contact, email, address, password, sq, sq_answer, window):
            if not all([username, fullname, contact, email, address, password, sq, sq_answer]):
                messagebox.showwarning("Input Error", "All fields are required!")
                return

            try:
                # Encode password and security answer
                encoded_password = str_encode(password)
                encoded_sq_answer = str_encode(sq_answer)

                # Insert into database
                conn = sqlite3.connect(DATABASE_FILE)
                c = conn.cursor()
                c.execute("""
                    INSERT INTO users (username, fullname, contact, email, address, password, securityquestion, securityanswer)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (username, fullname, contact, email, address, encoded_password, sq, encoded_sq_answer))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "User registered successfully!")
                refresh_table()  # Refresh the table
                window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username or email already exists!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        # Function to edit a user
        def edit_user():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select a user to edit.")
                return

            selected_user = tree.item(selected_item, "values")
            edit_window = Toplevel(root)
            edit_window.title("Edit User")
            edit_window.geometry("500x400")

            # Labels and Entries
            Label(edit_window, text="Username:").pack()
            username_entry = Entry(edit_window)
            username_entry.insert(0, selected_user[1])
            username_entry.pack()

            Label(edit_window, text="Full Name:").pack()
            fullname_entry = Entry(edit_window)
            fullname_entry.insert(0, selected_user[2])
            fullname_entry.pack()

            Label(edit_window, text="Contact:").pack()
            contact_entry = Entry(edit_window)
            contact_entry.insert(0, selected_user[3])
            contact_entry.pack()

            Label(edit_window, text="Email:").pack()
            email_entry = Entry(edit_window)
            email_entry.insert(0, selected_user[4])
            email_entry.pack()

            Label(edit_window, text="Address:").pack()
            address_entry = Entry(edit_window)
            address_entry.insert(0, selected_user[5])
            address_entry.pack()

            # Submit Button
            Button(edit_window, text="Submit", command=lambda: submit_edit(
                selected_user[0],  # user_id
                username_entry.get(),
                fullname_entry.get(),
                contact_entry.get(),
                email_entry.get(),
                address_entry.get(),
                edit_window
            )).pack()

        # Function to submit user edits
        def submit_edit(user_id, username, fullname, contact, email, address, window):
            if not all([username, fullname, contact, email, address]):
                messagebox.showwarning("Input Error", "All fields are required!")
                return

            try:
                conn = sqlite3.connect(DATABASE_FILE)
                c = conn.cursor()
                c.execute("""
                    UPDATE users
                    SET username = ?, fullname = ?, contact = ?, email = ?, address = ?
                    WHERE user_id = ?
                """, (username, fullname, contact, email, address, user_id))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "User updated successfully!")
                refresh_table()  # Refresh the table
                window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username or email already exists!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        # Function to delete a user
        def delete_user():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select a user to delete.")
                return

            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?"):
                user_id = tree.item(selected_item, "values")[0]
                try:
                    conn = sqlite3.connect(DATABASE_FILE)
                    c = conn.cursor()
                    c.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
                    conn.commit()
                    conn.close()
                    refresh_table()  # Refresh the table
                    messagebox.showinfo("Success", "User deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")

        # Function to filter users
        def filter_users(filter_by):
            for row in tree.get_children():
                tree.delete(row)

            if filter_by == "Username":
                sorted_rows = sorted(rows, key=lambda x: x[1].lower())
            elif filter_by == "Email":
                sorted_rows = sorted(rows, key=lambda x: x[4].lower())
            else:
                sorted_rows = rows

            for row in sorted_rows:
                tree.insert("", "end", values=row)

        # Function to search users
        def search_users():
            search_term = search_entry.get().strip().lower()

            for row in tree.get_children():
                tree.delete(row)

            filtered_rows = [row for row in rows if any(search_term in str(cell).lower() for cell in row)]

            for row in filtered_rows:
                tree.insert("", "end", values=row)

        # Function to display selected number of users
        def display_users(limit):
            for row in tree.get_children():
                tree.delete(row)

            if limit == "All":
                for row in rows:
                    tree.insert("", "end", values=row)
            else:
                for row in rows[:int(limit)]:
                    tree.insert("", "end", values=row)

        header = Label(main_frame, text='Users', font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10)


        # Rectangle stats no. frame

        stats_frame = Frame(main_frame, bg=MAINFRAME_COLOR)
        stats_frame.pack()
        stat_box = Frame(stats_frame, bg=BUTTON_COLOR, width=120, height=60)
        stat_box.pack_propagate(False)
        stat_box.pack(side=LEFT, padx=10, pady=10)
            
        stat_label = Label(stat_box, text=stats()[0][1], font=("Arial", 14, "bold"), fg=FG_COLOR, bg=BUTTON_COLOR)
        stat_label.pack()
        stat_desc = Label(stat_box, text='Total Users', font=("Arial", 10), fg=FG_COLOR, bg=BUTTON_COLOR)
        stat_desc.pack()

        # Search Bar
        search_frame = Frame(main_frame, bg=MAINFRAME_COLOR)
        search_frame.pack(padx=10, pady=10)

        Label(search_frame, text="Search:",bg=MAINFRAME_COLOR).pack(side="left", padx=5)
        search_entry = Entry(search_frame,font=button_font)
        search_entry.pack(side="left", padx=5, fill="x", expand=True)

        Button(search_frame, text="Search", command=search_users, bg=BUTTON_COLOR,font=button_font,fg=FG_COLOR).pack(side="left", padx=5)

        # Filter Option
        filter_frame = Frame(main_frame, bg=MAINFRAME_COLOR)
        filter_frame.pack(fill="x", padx=10, pady=10)

        Label(filter_frame, text="Filter By:",bg = MAINFRAME_COLOR).pack(side="left", padx=5)
        filter_var = StringVar(value="Username")
        OptionMenu(filter_frame, filter_var, "Username", "Email", command=filter_users).pack(side="left", padx=5)

        # Display Number of Users
        display_frame = Frame(main_frame, bg=MAINFRAME_COLOR)
        display_frame.pack(fill="x", padx=10, pady=10)

        Label(display_frame, text="Display:",bg=MAINFRAME_COLOR).pack(side="left", padx=5)
        display_var = StringVar(value="10")
        OptionMenu(display_frame, display_var, "5", "10", "15", "20", "25", "30", "50", "All", command=display_users).pack(side="left", padx=5)

        # Table
        columns = ("User ID", "Username", "Full Name", "Contact", "Email", "Address")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=CENTER, width=150)

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons
        button_frame = Frame(main_frame, bg=MAINFRAME_COLOR)
        button_frame.pack(fill="x", padx=10, pady=10)

        Button(button_frame, text="Add User", bg=BUTTON_COLOR, fg=FG_COLOR, command=register_user,font=button_font).pack(side="left", padx=5)
        Button(button_frame, text="Delete User", bg=LOGOUT_COLOR, fg=FG_COLOR, command=delete_user,font=button_font).pack(side="right", padx=5)
        Button(button_frame, text="Edit User", bg=BUTTON_COLOR, fg=FG_COLOR, command=edit_user,font=button_font).pack(side="right", padx=5)

        # Initial Table Refresh
        refresh_table()


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
            stat_label.config(text=len(get_courses()))
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


        # Database Connection Open
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()

        # demo courses creation or insertion
        # c.execute('SELECT * FROM courses')
        # cou = c.fetchall()
        # if not cou:
        #     for cn in defcourses:
        #         c.execute('INSERT INTO courses (coursename) VALUES (?)', (cn,))
        #     conn.commit()
    

        header = Label(main_frame, text="Courses and Categories", font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10)

        # Courses Section

        # Rectangle courses no. frame

        stats_frame = Frame(main_frame, bg=MAINFRAME_COLOR)
        stats_frame.pack()
        stat_box = Frame(stats_frame, bg=BUTTON_COLOR, width=120, height=60)
        stat_box.pack_propagate(False)
        stat_box.pack(side=LEFT, padx=10, pady=10)
            
        stat_label = Label(stat_box, text=stats()[1][1], font=("Arial", 14, "bold"), fg=FG_COLOR, bg=BUTTON_COLOR)
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

        columns = ('course_id', 'coursename')
        course_table = ttk.Treeview(course_table_frame, columns=columns, show='headings',height=5)
        course_table.heading('course_id', text='Course ID')
        course_table.heading('coursename', text='Course Name')
        # course_table.heading('actions', text='Actions')

        # Configure columns with center alignment
        course_table.column('course_id', anchor='center')
        course_table.column('coursename', anchor='center')
        # course_table.column('actions', anchor='center')

        # Create vertical scrollbar and link it to the Treeview
        course_v_scrollbar = ttk.Scrollbar(course_table_frame, orient='vertical', command=course_table.yview)
        course_v_scrollbar.pack(side='right', fill='y')
        course_table.configure(yscrollcommand=course_v_scrollbar.set)

        
        course_table.pack()


        # To display all courses at first
        update_course_table(get_courses())

        # EDIT / DELETE Buttons for Courses
        
        # When course table clicked

        def on_course_select(event):
            selected_item = course_table.focus()
            item_data = course_table.item(selected_item)
            return item_data
        
        course_table.bind('<<TreeviewSelect>>', on_course_select)

        def edit_course_record():
            def save_edit_course():
                if course_name_entry.get().isprintable():
                    try:
                        c.execute('UPDATE courses SET coursename = ? WHERE course_id = ?', (course_name_entry.get(), item_data["values"][0]))
                        conn.commit()
                        update_course_table(get_courses())
                        edit_course_window.destroy()
                        messagebox.showinfo(title='Success',message='Course Edited successfully.')
                    except Exception as e:
                        messagebox.showerror(title='Error in Editing Course',message='Edit Course Error: ' + str(e))
                else:
                    messagebox.showwarning(title='Black Data',message='Blank Data in Course Name.')

            def cancel_edit_course():
                edit_course_window.destroy()


            selected_item = course_table.focus()
            item_data = course_table.item(selected_item)
            if selected_item:
                # print("Edit item:", item_data['values'][0])
                edit_course_window = Toplevel(main_frame)
                edit_course_window.title('Add Course')
                edit_course_window.geometry('400x300')

                edit_course_window.resizable(False, False)  # Prevent window resizing
                edit_course_window.wm_attributes("-toolwindow", 1) # Disable max and min button

                edit_course_frame = Frame(edit_course_window,padx=10,pady=10,border=2,borderwidth=2)
                edit_course_frame.pack()

                # Frame for the first row
                edit_course_row1 = Frame(edit_course_window, padx=10, pady=10, border=2, borderwidth=2)
                edit_course_row1.pack(fill='x')

                course_name_label = Label(edit_course_row1, text='Course Name', font=("Arial", 14))
                course_name_label.pack(side='left', pady=5, padx=5)

                course_name_entry = Entry(edit_course_row1, font=("Arial", 12))
                course_name_entry.pack(side='right', padx=5)
                course_name_entry.insert(0, item_data["values"][1])

                # Frame for the second row
                edit_course_row2 = Frame(edit_course_window, padx=10, pady=10, border=2, borderwidth=2)
                edit_course_row2.pack(fill='x')

                save_course_btn = Button(edit_course_row2, text='Save', command=save_edit_course, font=("Arial", 12), fg='white', bg='blue')
                save_course_btn.pack(side='left', padx=5, pady=5)

                close_course_btn = Button(edit_course_row2, text='Cancel', command=cancel_edit_course, font=("Arial", 12), fg='white', bg='red')
                close_course_btn.pack(side='right', padx=5, pady=5)
            pass

        def delete_course_record():
            selected_item = course_table.focus()
            item_data = course_table.item(selected_item)

            if selected_item:
                confirm = messagebox.askokcancel("Confirm Delete", f"Are you sure you want to delete {item_data['values'][1]}?")
                if confirm:
                    c.execute('DELETE FROM courses WHERE course_id = ?', (item_data["values"][0],))
                    conn.commit()
                    update_course_table(get_courses())
                    stat_label.config(text=stats()[1][1])
                

        course_action_frame = Frame(main_frame,bg=MAINFRAME_COLOR)
        course_action_frame.pack()

        Label(course_action_frame,text='Select a Record to be Edited or Deleted.',font=label_font,bg=MAINFRAME_COLOR).pack()

        edit_button = Button(course_action_frame, text="Edit",font=button_font, bg=BUTTON_COLOR, fg=FG_COLOR, relief=FLAT,command=edit_course_record)
        edit_button.pack(side=LEFT, padx=10, pady=10)

        delete_button = Button(course_action_frame, text="Delete", bg=LOGOUT_COLOR, fg=FG_COLOR, relief=FLAT,font=button_font,command=delete_course_record)
        delete_button.pack(side=RIGHT, padx=10, pady=10)


        # Categories section

        # Categories Functions

        def add_category():

            def save_category():
                if category_name_entry.get().isprintable():
                    try:
                        # print(next((course for course in get_courses() if course[1] == selected_course.get()),None))
                        c.execute('INSERT INTO categories (category_name, course_id) VALUES (?,?)', (category_name_entry.get(),next((course[0] for course in get_courses() if course[1] == selected_course.get()),None)))
                        conn.commit()
                        add_category_window.destroy()
                        update_category_table(get_categories())
                        messagebox.showinfo(title='Success',message='Course successfully created.')
                    except Exception as e:
                        messagebox.showerror(title='Error in Adding Categories',message='Save Category Error: ' + str(e))
                else:
                    messagebox.showwarning(title='Black Data',message='Blank Data in Category Name.')

            def cancel_category():
                add_category_window.destroy()

            add_category_window = Toplevel(main_frame)
            add_category_window.title('Add Category')
            add_category_window.geometry('400x300')

            add_category_window.resizable(False, False)  # Prevent window resizing
            add_category_window.wm_attributes("-toolwindow", 1) # Disable max and min button

            # conn = sqlite3.connect(DATABASE_FILE)
            # c = conn.cursor()

            add_category_frame = Frame(add_category_window,padx=10,pady=10,border=2,borderwidth=2)
            add_category_frame.pack()
            
            # Frame for the first row
            category_row1 = Frame(add_category_window, padx=10, pady=10, border=2, borderwidth=2)
            category_row1.pack(fill='x')

            category_name_label = Label(category_row1, text='Category Name', font=("Arial", 14))
            category_name_label.pack(side='left', pady=5, padx=5)

            category_name_entry = Entry(category_row1, font=("Arial", 12))
            category_name_entry.pack(side='right', padx=5)

            # Frame for the second row
            category_row2 = Frame(add_category_window, padx=10, pady=10, border=2, borderwidth=2)
            category_row2.pack(fill='x')

            course_name_label = Label(category_row2, text='Select Course', font=("Arial", 14))
            course_name_label.pack(side='left', pady=5, padx=5)

            selected_course = StringVar()
            course_options = [course[1] for course in get_courses()]
            selected_course.set(course_options[0] if course_options[0] is not None else "No Course Added" )

            course_dropdown = OptionMenu(category_row2, selected_course, *course_options)
            course_dropdown.pack(side='right', padx=5)

            # Frame for the buttons row
            category_button_row_frame = Frame(add_category_window, padx=10, pady=10, border=2, borderwidth=2)
            category_button_row_frame.pack(fill='x')

            save_category_btn = Button(category_button_row_frame, text='Save', command=save_category, font=("Arial", 12), fg='white', bg='blue')
            save_category_btn.pack(side='left', padx=5, pady=5)

            close_category_btn = Button(category_button_row_frame, text='Cancel', command=cancel_category, font=("Arial", 12), fg='white', bg='red')
            close_category_btn.pack(side='right', padx=5, pady=5)

        def update_category_table(results):
            for row in category_table.get_children():
                category_table.delete(row)
            for row in results:
                category_table.insert('', 'end', values=row)

        # All categories data with coursename
        def get_categories():
            
            c.execute('SELECT * FROM categories')
            categories = c.fetchall()
            categories = [list(category) for category in categories]
            # print(categories)
            courses = get_courses()
            # print(courses)

            for category in categories:
                for course in courses:
                    if category[2] == course[0]:
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

        columns = ('category_id', 'categoryname','coursename')
        category_table = ttk.Treeview(category_table_frame, columns=columns, show='headings',height=5)
        category_table.heading('category_id', text='Category ID')
        category_table.heading('categoryname', text='Category Name')
        category_table.heading('coursename', text='Course Name')
        # category_table.heading('actions', text='Actions')

        # Configure columns with center alignment
        category_table.column('category_id', anchor='center')
        category_table.column('categoryname', anchor='center')
        category_table.column('coursename', anchor='center')
        # category_table.column('actions', anchor='center')

        # Create vertical scrollbar and link it to the Treeview
        category_v_scrollbar = ttk.Scrollbar(category_table_frame, orient='vertical', command=category_table.yview)
        category_v_scrollbar.pack(side='right', fill='y')
        category_table.configure(yscrollcommand=category_v_scrollbar.set)

        category_table.pack()

        # c.execute('UPDATE categories SET course_id = 1 WHERE category_id = 1')
        # conn.commit()

        # To display all courses at first
        update_category_table(get_categories())

        # Edit and Delete Button Functions


        # On click in category record

        def on_category_select(event):
            selected_item = category_table.focus()
            item_data = category_table.item(selected_item)
            return item_data

        category_table.bind('<<TreeviewSelect>>', on_category_select)

        def edit_category_record():
            def save_edit_category():
                try:
                    c.execute('UPDATE categories SET category_name = ?,course_id = ? WHERE category_id = ?', (category_name_entry.get(),next((course[0] for course in get_courses() if course[1] == selected_course.get()),None),item_data["values"][0]))
                    conn.commit()
                    update_category_table(get_categories())
                    edit_category_window.destroy()
                    messagebox.showinfo(title='Success',message='Category Edited successfully.')
                except Exception as e:
                    messagebox.showerror(title='Error in Editing Category',message='Edit Category Error: ' + str(e))

            def cancel_edit_category():
                edit_category_window.destroy()


            selected_item = category_table.focus()
            item_data = category_table.item(selected_item)
            if selected_item:
                # print("Edit item:", item_data['values'][0])
                edit_category_window = Toplevel(main_frame)
                edit_category_window.title('Add Course')
                edit_category_window.geometry('400x300')

                edit_category_window.resizable(False, False)  # Prevent window resizing
                edit_category_window.wm_attributes("-toolwindow", 1) # Disable max and min button

                edit_category_frame = Frame(edit_category_window,padx=10,pady=10,border=2,borderwidth=2)
                edit_category_frame.pack()

                # Frame for the first row
                edit_category_row1 = Frame(edit_category_window, padx=10, pady=10, border=2, borderwidth=2)
                edit_category_row1.pack(fill='x')

                category_name_label = Label(edit_category_row1, text='Course Name', font=("Arial", 14))
                category_name_label.pack(side='left', pady=5, padx=5)

                category_name_entry = Entry(edit_category_row1, font=("Arial", 12))
                category_name_entry.pack(side='right', padx=5)
                category_name_entry.insert(0, item_data["values"][1])

                # Frame for the second row
                edit_category_row2 = Frame(edit_category_window, padx=10, pady=10, border=2, borderwidth=2)
                edit_category_row2.pack(fill='x')

                course_name_label = Label(edit_category_row2, text='Change Course', font=("Arial", 14))
                course_name_label.pack(side='left', pady=5, padx=5)

                selected_course = StringVar()
                course_options = [course[1] for course in get_courses()]
                selected_course.set(item_data["values"][2])

                course_dropdown = OptionMenu(edit_category_row2, selected_course, *course_options)
                course_dropdown.pack(side='right', padx=5)

                # Frame for the buttons row
                edit_category_button_row_frame = Frame(edit_category_window, padx=10, pady=10, border=2, borderwidth=2)
                edit_category_button_row_frame.pack(fill='x')

                save_category_btn = Button(edit_category_button_row_frame, text='Save', command=save_edit_category, font=("Arial", 12), fg='white', bg='blue')
                save_category_btn.pack(side='left', padx=5, pady=5)

                close_category_btn = Button(edit_category_button_row_frame, text='Cancel', command=cancel_edit_category, font=("Arial", 12), fg='white', bg='red')
                close_category_btn.pack(side='right', padx=5, pady=5)
            pass

        def delete_category_record():
            selected_item = category_table.focus()
            item_data = category_table.item(selected_item)

            if selected_item:
                confirm = messagebox.askokcancel("Confirm Delete", f"Are you sure you want to delete {item_data['values'][1]} from {item_data['values'][2]}?")
                if confirm:
                    c.execute('DELETE FROM categories WHERE category_id = ?', (item_data["values"][0],))
                    conn.commit()
                    update_category_table(get_categories())

        # EDIT / DELETE Buttons for Courses

        category_action_frame = Frame(main_frame,bg=MAINFRAME_COLOR)
        category_action_frame.pack()

        Label(category_action_frame,text='Select a Record to be Edited or Deleted.',font=label_font,bg=MAINFRAME_COLOR).pack()

        edit_button = Button(category_action_frame, text="Edit",font=button_font, bg=BUTTON_COLOR, fg=FG_COLOR, relief=FLAT,command=edit_category_record)
        edit_button.pack(side=LEFT, padx=10, pady=10)

        delete_button = Button(category_action_frame, text="Delete", bg=LOGOUT_COLOR, fg=FG_COLOR, relief=FLAT,font=button_font,command=delete_category_record)
        delete_button.pack(side=RIGHT, padx=10, pady=10)

        # Close DB Connection
        conn.commit()
        # conn.close()


    # Leaderboard - admin section
    elif btn_text == buttons[3]:
        
        # Replace all date string parsing with direct date object usage
        def get_formatted_dates():
            # Get dates directly from widgets
            date_from_obj = date_from.get_date()
            date_to_obj = date_to.get_date()
            
            # Format for SQL comparison
            return (
                date_from_obj.strftime("%Y-%m-%d 00:00:00"),
                date_to_obj.strftime("%Y-%m-%d 23:59:59")
            )
        
        def refresh_data(event=None):
            # Get current filters
            query = search_entry.get().strip()
            selected_course_name = selected_course.get()
            
            # Resolve user ID if search query exists
            user_id = None
            if query:
                conn = sqlite3.connect(DATABASE_FILE)
                c = conn.cursor()
                c.execute("SELECT user_id FROM users WHERE username = ?", (query,))
                user_data = c.fetchone()
                conn.close()
                if user_data:
                    user_id = user_data[0]
                else:
                    messagebox.showinfo("Not Found", f"User '{query}' not found")
                    return

            # Resolve course ID
            course_id = None
            if selected_course_name != "All":
                conn = sqlite3.connect(DATABASE_FILE)
                c = conn.cursor()
                c.execute("SELECT course_id FROM courses WHERE coursename = ?", (selected_course_name,))
                course_data = c.fetchone()
                conn.close()
                if course_data:
                    course_id = course_data[0]

            # Get results with current filters
            results = get_mocktest_results(user_id=user_id, course_id=course_id)
            populate_table(results)
        
        # Search function to filter by username
        def search():
            query = search_entry.get().strip()
            if not query:
                messagebox.showwarning("Search", "Please enter a username")
                return

            conn = sqlite3.connect(DATABASE_FILE)
            c = conn.cursor()
            c.execute("SELECT user_id FROM users WHERE username = ?", (query,))
            user_data = c.fetchone()
            conn.close()
            
            if not user_data:
                messagebox.showinfo("Not Found", f"User '{query}' not found")
                return

            # Get course filter
            selected_course_name = selected_course.get()
            course_id = None
            if selected_course_name != "All":
                conn = sqlite3.connect(DATABASE_FILE)
                c = conn.cursor()
                c.execute("SELECT course_id FROM courses WHERE coursename = ?", (selected_course_name,))
                course_data = c.fetchone()
                conn.close()
                if course_data:
                    course_id = course_data[0]

            results = get_mocktest_results(user_id=user_data[0], course_id=course_id)
            populate_table(results)

        def course_selected(selected_course_name):
            refresh_data()  # Simplified to call unified refresh
            
        
            
        def get_mocktest_results(user_id=None, course_id=None):
            conn = sqlite3.connect(DATABASE_FILE)
            c = conn.cursor()

            query = """
                SELECT 
                    u.username, 
                    c.coursename, 
                    SUM(m.result) AS total_score
                FROM mocktestresults m
                JOIN users u ON m.user_id = u.user_id
                JOIN courses c ON m.course_id = c.course_id
                WHERE m.resulttime BETWEEN ? AND ?
            """

            params = []
            
            # Add date filter (always applied)
            date_start, date_end = get_formatted_dates()
            params.extend([date_start, date_end])

            # Add optional filters
            if user_id:
                query += " AND m.user_id = ?"
                params.append(user_id)
            if course_id:
                query += " AND m.course_id = ?"
                params.append(course_id)

            query += " GROUP BY m.user_id, m.course_id ORDER BY total_score DESC"

            c.execute(query, tuple(params))
            results = c.fetchall()
            conn.close()
            return results
            
                
        def populate_table(results):
            # Clear existing data
            for item in table.get_children():
                table.delete(item)
            
            # Insert new data with proper ordering
            for idx, row in enumerate(results, 1):
                table.insert("", "end", values=(
                    idx,        # Serial Number
                    row[1],    # Course Name
                    row[0],    # Username
                    row[2]     # Total Score
                ))
                
        header = Label(main_frame, text="Leaderboard", font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10)
                
            # Search Section
        searchfr = Frame(main_frame, bg=MAINFRAME_COLOR)
        searchfr.place(x=80, y=250, width=305, height=50)
        search_entry = Entry(searchfr, width=15, font=("Arial", 14))
        search_entry.place(x=5, y=10)
        search_button = Button(searchfr, text="Search", font=("Arial", 12), command=search, bg=BUTTON_COLOR,fg=FG_COLOR)
        search_button.place(x=215, y=5)

        # Course Selection
        course_frame = Frame(main_frame, bg=MAINFRAME_COLOR)
        course_frame.place(x=400, y=250, width=305, height=50)
        courses = ['All']+[coursename[1] for coursename in get_courses()]
        selected_course = StringVar(value="Choose course")
        course_menu = OptionMenu(course_frame, selected_course, *courses, command=course_selected)
        course_menu.config(font=("Arial", 12), width=20,bg=BUTTON_COLOR,fg=FG_COLOR)
        course_menu.place(x=15, y=4)

        # Date Selection
        
        current_date = date.today()
        first_day_of_month = current_date.replace(day=1)
            
        
        Label(main_frame, text="From:", font=('Arial', 14),bg=MAINFRAME_COLOR).place(x=925, y=260)
        date_from = DateEntry(
            main_frame, 
            width=15, 
            font=('Arial', 14),
            date_pattern="mm/dd/yyyy"
        )        
        date_from.place(x=1000, y=260)

        Label(main_frame, text="To:", font=('Arial', 14),bg=MAINFRAME_COLOR).place(x=1250, y=260)
        date_to = DateEntry(
            main_frame,
            width=15, 
            font=('Arial', 14),
            date_pattern="mm/dd/yyyy"
        )        
        date_to.place(x=1300, y=260)

        date_from.set_date(datetime.now().replace(day=1))
        date_to.set_date(datetime.now())
        
        # After creating DateEntry widgets
        date_from.bind("<<DateEntrySelected>>", refresh_data)
        date_to.bind("<<DateEntrySelected>>", refresh_data)
        
        # Table Frame (Treeview)
        table_frame = Frame(main_frame, bd=2, relief="ridge")
        table_frame.place(x=350, y=325, width=1000, height=600)

        # Creating Treeview table
        columns = ("SN", "Course", "Username", "Score")
        table = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Defining column headings
        for col in columns:
            table.heading(col, text=col)
            table.column(col, anchor="center", width=150)

        # Adding Scrollbars
        scroll_y = Scrollbar(table_frame, orient=VERTICAL, command=table.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        table.configure(yscrollcommand=scroll_y.set)

        # Placing the table
        table.pack(expand=True, fill=BOTH)

        # Load initial data after UI setup
        def load_initial_data():
            results = get_mocktest_results()
            populate_table(results)

        # Call this after all widgets are created
        load_initial_data()
        
        pass

    # Mocktest - admin section - aayush
    elif btn_text == buttons[4]:

        #header section
        header = Label(main_frame, text="Mock Test", font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10)
    
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
            add_mocktest = Toplevel(main_frame)
            add_mocktest.title("Add Questions To Mock Test")
            add_mocktest.geometry("800x300")
            add_mocktest.attributes('-topmost', True)
    
            Label(add_mocktest, text="Enter Mock Test Name:").pack()
            e1 = Entry(add_mocktest, width=35)
            e1.pack(pady=10)

            Label(add_mocktest, text="Enter Mock Test description:").pack()
            text_desc = Text(add_mocktest,height=2, width=40)
            text_desc.pack(pady=10)
            
            Label(add_mocktest, text="Enter Full Marks:").pack()
            e2 = Entry(add_mocktest, width=35)
            e2.pack(pady=10)

            Label(add_mocktest, text="Enter Pass Marks:").pack()
            e3 = Entry(add_mocktest, width=35)
            e3.pack(pady=10)

            

            Label(add_mocktest, text="Enter Pass Marks:").pack()
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
                    
                    
            
            #Button(add_mocktest, text="Save", command=save_mock).pack()

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
            add_question_window = Toplevel(main_frame)
            add_question_window.title("Add Questions To Mock Test")
            add_question_window.geometry("600x300")
            course_id = None
            category_id = None
            add_question_window.attributes('-topmost', True)
           

            Label(add_question_window, text="Mock Test Name:").pack()
            test_names = [test[1] for test in fetch_mock_tests()]
            mock_test_combo = ttk.Combobox(add_question_window, values=test_names, state='readonly')
            mock_test_combo.pack()
            
            Label(add_question_window, text="Courses:").pack()
            course_names = [test[1] for test in fetch_courses()]
            courses_combo = ttk.Combobox(add_question_window, values= course_names, state='readonly')
            courses_combo.pack()
            
            Label(add_question_window, text="Categories:").pack()
            
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
            
            Label(add_question_window, text="No of Questions:").pack()
            questions_entry = Entry(add_question_window)
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
        
             #Button(add_question_window, text="Save", command=save_question).pack()

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

    # Question - admin section - aayush
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
            add_window = Toplevel(main_frame)
            add_window.title("Add Question")
            add_window.geometry("600x450")

            #Courses
            Label(add_window, text="Courses:").pack()
            course_names = [test[1] for test in fetch_courses()]
            courses_combo = ttk.Combobox(add_window, values= course_names, state='readonly')
            courses_combo.pack(pady=10)

            #Category   
            Label(add_window, text="Categories:").pack()
             
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
            Label(add_window,text='Enter question:').pack()
            #question_box = Entry(add_window, width=35)
            #question_box.pack()
            question_box= Text(add_window,height= 5,width= 40)
            question_box.pack(pady=10)
            
            Label(add_window, text="Incorrect answer:").pack()
            #Incorrect_box = Entry(add_window, width=35)
            #Incorrect_box.pack()
            Incorrect_box = Text(add_window, height= 2, width = 40)
            Incorrect_box.pack(pady=10)

            Label(add_window, text="Correct answer:").pack()
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
                
        
            #Button(add_window, text="Save", command=save_question).pack()

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
            
           
            edit_window = Toplevel(main_frame)
            edit_window.title("Edit Question")
            edit_window.geometry("600x450")

            #Courses
            Label(edit_window, text="Courses:").pack()

            # Fetch courses and set default selection
            course_names = [course[1] for course in fetch_courses()]
            c_name = StringVar()
            c_name.set(selected_question[4])  # Default selection

            # Create Course ComboBox
            courses_combo = ttk.Combobox(edit_window, textvariable=c_name, values=course_names, state="readonly")
            courses_combo.pack(pady=10)

            # Label for Categories
            Label(edit_window, text="Categories:").pack()

            # Fetch initial categories based on the default course
            default_course_id = next((course[0] for course in fetch_courses() if course[1] == c_name.get()), None)
            category_names = [category[1] for category in fetch_categories(default_course_id)]

            # Create Category ComboBox
            ca_name = StringVar()
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
            Label(edit_window,text='Enter question:').pack()
            question_box = Text(edit_window, height=5,width=40)
            question_box.insert('1.0',selected_question[1])
            question_box.pack(pady = 10)

            Label(edit_window, text="Incorrect answer:").pack()
            Incorrect_box = Text(edit_window,height=2, width=40)
            Incorrect_box.insert('1.0',selected_question[3])
            Incorrect_box.pack(pady=10)

            Label(edit_window, text="Correct answer:").pack()
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

        question_column = ["Id", "Question", "Correct","Incorrect",  "Courses", "Category"]
        questions_table = ttk.Treeview(questiontable_frame, columns=question_column, show="headings")

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

def logout():
    root.destroy()
    runpy.run_path(r'..\quizapp-tkinter\app\welcome.py')
    pass

logout_btn = Button(sidebar, text="🔓 LogOut", bg=LOGOUT_COLOR, fg=FG_COLOR, relief=FLAT, width=20, height=2,command=logout)
logout_btn.pack(pady=20)

# Main Dashboard
main_frame = Frame(root, bg=MAINFRAME_COLOR)
main_frame.pack(expand=True, fill=BOTH)

# Initialize with Dashboard
openbutton(buttons[0])

root.mainloop()
