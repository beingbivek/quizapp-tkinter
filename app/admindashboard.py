from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
from PIL import ImageTk, Image
import runpy
import sqlite3
from tkinter import simpledialog
import tkinter as tk
from tkcalendar import DateEntry

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

         # Data from all tables
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute('SELECT * FROM sqlite_sequence')
        stat_data = c.fetchall()
        conn.commit()
        conn.close()

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

    # Modify the `elif btn_text == buttons[1]:` section
    elif btn_text == buttons[1]:
        # Clear the main frame
        for widget in main_frame.winfo_children():
            widget.destroy()

        # Function to fetch users from the database
        def fetch_users():
            try:
                conn = sqlite3.connect('quiz.db')  # Replace with your actual database name
                c = conn.cursor()
                c.execute("SELECT user_id, username, fullname, contact, email FROM users")
                users = c.fetchall()
                conn.close()
                print("Fetched Users:", users)  # Debugging: Print fetched data
                return users
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while fetching users: {e}")
                return []

        # Function to refresh the table with data from the database
        def refresh_table():
            global rows
            rows = fetch_users()  # Fetch users from the database
            print("Rows Data:", rows)  # Debugging: Print rows data
            for row in tree.get_children():
                tree.delete(row)  # Clear the existing rows in the table
            for row in rows:
                tree.insert("", "end", values=row)  # Insert fetched data into the table
            tree.configure(height=len(rows))

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

        # Fetch and display users from the database
        refresh_table()

        # Ensure the Treeview is placed correctly
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
            try:
                conn = sqlite3.connect('quiz.db')  # Replace with your actual database name
                c = conn.cursor()
                c.execute("""
                    INSERT INTO users (username, fullname, contact, email, password)
                    VALUES (?, ?, ?, ?, ?)
                """, (username, name, contact, email, "default_password"))  # Replace "default_password" with actual password handling
                conn.commit()
                conn.close()
                refresh_table()  # Refresh the table after adding a new user
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

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
            try:
                user_id = tree.item(selected_item, "values")[0]
                conn = sqlite3.connect('quiz.db')  # Replace with your actual database name
                c = conn.cursor()
                c.execute("""
                    UPDATE users
                    SET username = ?, fullname = ?, contact = ?, email = ?
                    WHERE user_id = ?
                """, (username, name, contact, email, user_id))
                conn.commit()
                conn.close()
                refresh_table()  # Refresh the table after editing
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        def delete_user():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select a user to delete.")
                return

            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?"):
                user_id = tree.item(selected_item, "values")[0]
                try:
                    conn = sqlite3.connect('quiz.db')  # Replace with your actual database name
                    c = conn.cursor()
                    c.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
                    conn.commit()
                    conn.close()
                    refresh_table()  # Refresh the table after deletion
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")


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
    

        header = Label(main_frame, text="Courses", font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10)

        # Courses Section

        # Rectangle courses no. frame

        stats_frame = Frame(main_frame, bg=MAINFRAME_COLOR)
        stats_frame.pack()
        stat_box = Frame(stats_frame, bg=BUTTON_COLOR, width=120, height=60)
        stat_box.pack_propagate(False)
        stat_box.pack(side=LEFT, padx=10, pady=10)
            
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
        def search():
            query = search_entry.get()
            if query:
                messagebox.showinfo("Search", f"You searched for: {query}")
            else:
                messagebox.showwarning("Search", "Please enter a search term.")

        def course_selected(selected_course):
            messagebox.showinfo("Course Selected", f"You selected: {selected_course}")
            populate_table(selected_course)

        def populate_table(selected_course):
            # Clear the previous data in Treeview
            for item in table.get_children():
                table.delete(item)

            # Sample table data
            data = [
                [1, selected_course, "User1", "90"],
                [2, selected_course, "User2", "85"],
                [3, selected_course, "User3", "75"],
                [4, selected_course, "User4", "80"],
            ]

            # Insert new data into the table
            for row in data:
                table.insert("", "end", values=row)
                
        header = Label(main_frame, text="Leaderboard", font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10)
                
            # Search Section
        searchfr = Frame(main_frame, bd=2, relief="ridge", bg="lightgrey")
        searchfr.place(x=420, y=200, width=305, height=50)
        search_entry = Entry(searchfr, width=15, font=("Arial", 14))
        search_entry.place(x=90, y=8)
        search_button = Button(searchfr, text="Search", font=("Arial", 12), command=search)
        search_button.place(x=5, y=4)

        # Course Selection
        course_frame = Frame(main_frame, bd=2, relief="ridge", bg="lightgrey")
        course_frame.place(x=420, y=300, width=305, height=50)
        courses = ["Loksewa", "CEE", "IOE", "Driving"]
        selected_course = StringVar(value="Choose course")
        course_menu = OptionMenu(course_frame, selected_course, *courses, command=course_selected)
        course_menu.config(font=("Arial", 12), width=20)
        course_menu.place(x=15, y=4)

        # Date Selection
        Label(main_frame, text="From:", font=('Arial', 14),bg=PROFILE_COLOR).place(x=1125, y=200)
        date_from = DateEntry(main_frame, width=15, font=('Arial', 14), background='darkblue', foreground='white', borderwidth=2)
        date_from.place(x=1200, y=200)

        Label(main_frame, text="To:", font=('Arial', 14),bg=PROFILE_COLOR).place(x=1125, y=250)
        date_to = DateEntry(main_frame, width=15, font=('Arial', 14), background='darkblue', foreground='white', borderwidth=2)
        date_to.place(x=1200, y=250)

        # Table Frame (Treeview)
        table_frame = Frame(main_frame, bd=2, relief="ridge")
        table_frame.place(x=550, y=500, width=700, height=250)

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

        populate_table("Loksewa")  # Default table population
        
        pass

    # Mocktest - admin section - aayush
    elif btn_text == buttons[4]:

        #header section
        header = Label(main_frame, text="Mock Test", font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10)

        # def setup_database():
        #     conn = sqlite3.connect(DATABASE_FILE)
        #     cursor = conn.cursor()

        #     # Create mocktests table
        #     cursor.execute('''
        #         CREATE TABLE IF NOT EXISTS mocktests (
        #             mocktest_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #             mocktest_name TEXT NOT NULL,
        #             fullmark INTEGER NOT NULL,
        #             passmark INTEGER NOT NULL
        #         )
        #     ''')

        #     # Create courses table
        #     cursor.execute('''
        #         CREATE TABLE IF NOT EXISTS courses (
        #             course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #             course_name TEXT NOT NULL
        #         )
        #     ''')

        #     # Create categories table
        #     cursor.execute('''
        #         CREATE TABLE IF NOT EXISTS categories (
        #             category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #             category_name TEXT NOT NULL
        #         )
        #     ''')

        #     # Create mockquestions table
        #     cursor.execute('''
        #         CREATE TABLE IF NOT EXISTS mockquestions (
        #             mockquestion_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #             mocktest_id INTEGER NOT NULL,
        #             course_id INTEGER NOT NULL,
        #             category_id INTEGER NOT NULL,
        #             no_of_questions INTEGER NOT NULL,
        #             FOREIGN KEY (mocktest_id) REFERENCES mocktests (mocktest_id),
        #             FOREIGN KEY (course_id) REFERENCES courses (course_id),
        #             FOREIGN KEY (category_id) REFERENCES categories (category_id)
        #         )
        #     ''')

        #     conn.commit()
        #     conn.close()

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
            global get_categories
            for question in fetch_questions():
                mocktest_name = next((test[1] for test in fetch_mock_tests() if test[0] == question[1]), None)
                course_name = next((test[1] for test in get_courses() if test[0] == question[2]), None)
                category_name = next((test[1] for test in get_categories() if test[0] == question[3]), None)
                # print(category_name)
                questions_table.insert("", "end", values=(question[0], mocktest_name, course_name, category_name, question[4]))
        
        #Function to add mocktest name, full marks, passmarks
        def add_mock_test():
            add_mocktest = Toplevel(main_frame)
            add_mocktest.title("Add Questions To Mock Test")
            add_mocktest.geometry("500x400")

            Label(add_mocktest, text="Enter Mock Test Name:").pack()
            e1 = Entry(add_mocktest, width=35)
            e1.pack()
            Label(add_mocktest, text="Enter Full Marks:").pack()
            e2 = Entry(add_mocktest, width=35)
            e2.pack()
            Label(add_mocktest, text="Enter Pass Marks:").pack()
            e3 = Entry(add_mocktest, width=35)
            e3.pack()

            #saves the input taken from admin 
            def save_mock():
                mocktest_name = e1.get().strip()  # Get the value and strip whitespace
                full_marks = e2.get().strip()      # Get the value and strip whitespace
                pass_marks = e3.get().strip()       # Get the value and strip whitespace
        
        # Check if any field is empty
                if not mocktest_name or not full_marks or not pass_marks:
                   messagebox.showwarning("Warning", "Please fill in all fields.")
                   return
            
                try:
                  conn = sqlite3.connect("quiz.db")
                  cursor = conn.cursor()
                  cursor.execute("INSERT INTO mocktests (mocktest_name, fullmark, passmark) VALUES (?, ?, ?)", 
                            (mocktest_name,full_marks,pass_marks))
                  conn.commit()
                  conn.close()
                  update_mock_test_table()
                  messagebox.showinfo("Success", "Test added successfully!")
                except sqlite3.IntegrityError:
                                messagebox.showerror("Error", "Mock test with this name already exists.")
                    
            
            Button(add_mocktest, text="Save", command=save_mock).pack()
        
        #function to add questions to specific test, corse, category
        def add_mock_question():
            add_question_window = Toplevel(main_frame)
            add_question_window.title("Add Questions To Mock Test")
            add_question_window.geometry("500x400")

            Label(add_question_window, text="Mock Test Name:").pack(side=LEFT)
            test_names = [test[1] for test in fetch_mock_tests()]
            mock_test_combo = ttk.Combobox(add_question_window, values=test_names)
            mock_test_combo.pack(side=RIGHT)
            
            Label(add_question_window, text="Courses:").pack(side=LEFT)
            course_names = [test[1] for test in get_courses()]
            courses_combo = ttk.Combobox(add_question_window, values= course_names)
            courses_combo.pack(side=RIGHT)
            
            Label(add_question_window, text="Categories:").pack()
            
            categories_combo = ttk.Combobox(add_question_window)
            categories_combo.pack()

            # Update categories based on selected course
            def update_categories(event):
                selected_course_name = courses_combo.get()
                course_id = next((course[0] for course in get_courses() if course[1] == selected_course_name), None)
                if course_id:
                    category_names = [category[1] for category in get_categories(course_id)]
                    categories_combo['values'] = category_names
                    categories_combo.set('')  # Clear the current selection

            courses_combo.bind("<<ComboboxSelected>>", update_categories)  # Bind the event
            
            Label(add_question_window, text="No of Questions:").pack()
            questions_entry = Entry(add_question_window)
            questions_entry.pack()

            def save_question():
                selected_test = mock_test_combo.get()
                course = courses_combo.get()
                category = categories_combo.get()
                num_questions = questions_entry.get()
                global get_categories
                
                if not (selected_test and course and category and num_questions.isdigit()):
                    messagebox.showerror("Error", "Please fill all fields correctly.")
                    return
                mock_test_id = next((test[0] for test in fetch_mock_tests() if test[1] == selected_test), None)
                course_id = next((test[0] for test in get_courses() if test[1] == course), None)
                category_id = next((cat[0] for cat in get_categories(course_id) if cat[1] == category), None)

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
        
            Button(add_question_window, text="Save", command=save_question).pack()
    
        # Updates the mock test table with every change
        def update_mock_test_table():
            for row in mock_test_table.get_children():
                mock_test_table.delete(row)
            for test in fetch_mock_tests():
                mock_test_table.insert("", "end", values=(test[0], test[1], test[2], test[3]))

       
        # setup_database()
        
        #main frame for table
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

        delete_btn = Button(btn_frame, text="Delete", command=delete_mock_test, bg= BUTTON_COLOR, font= button_font, fg= FG_COLOR  )
        delete_btn.pack(side=LEFT, padx=10)
        

        #question table
        questions_table = ttk.Treeview(main_frame, columns=("ID", "Mock Test-Name", "Course-Name", "Category", "Questions"), show="headings")
        for col in ["ID", "Mock Test-Name", "Course-Name", "Category", "Questions"]:
               questions_table.heading(col, text=col)
        questions_table.pack()

        delete_btn = Button(btn_frame, text="Delete QNs", command=delete_selected_question, bg= BUTTON_COLOR, font= button_font, fg= FG_COLOR  )
        delete_btn.pack(side=LEFT, padx=10)
        


        update_mock_test_table()
        update_questions_table()



    # Question - admin section - aayush
    elif btn_text == buttons[5]:

        header = Label(main_frame, text="Question", font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10)


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
