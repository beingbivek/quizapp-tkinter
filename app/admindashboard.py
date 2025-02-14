from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
from PIL import ImageTk, Image
import runpy
import sqlite3

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
        header = Label(main_frame, text=buttons[1], font=header_font, bg=MAINFRAME_COLOR)
        header.pack(pady=10)

        stats_frame = Frame(main_frame, bg=MAINFRAME_COLOR)
        stats_frame.pack()

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
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        pass

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
