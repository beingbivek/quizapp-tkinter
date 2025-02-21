from tkinter import *
from tkinter import messagebox
from tkinter import ttk  # Import ttk for Treeview
from tkcalendar import DateEntry  # Import DateEntry for date selection

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

# Initialize main window
root = Tk()
root.geometry('1000x800')
root.title('Leaderboard')

# Main frame
mainframe = Frame(root, bd=2, relief="ridge")
mainframe.place(x=0, y=0, width=1000, height=800)

# Search Section
searchfr = Frame(root, bd=2, relief="ridge", bg="lightgrey")
searchfr.place(x=20, y=200, width=300, height=50)
search_entry = Entry(searchfr, width=20, font=("Arial", 14))
search_entry.place(x=90, y=8)
search_button = Button(searchfr, text="Search", font=("Arial", 12), command=search)
search_button.place(x=10, y=5)

# Course Selection
course_frame = Frame(root, bd=2, relief="ridge", bg="lightgrey")
course_frame.place(x=350, y=200, width=280, height=50)
courses = ["Loksewa", "CEE", "IOE", "Driving"]
selected_course = StringVar(value="Choose course")
course_menu = OptionMenu(course_frame, selected_course, *courses, command=course_selected)
course_menu.config(font=("Arial", 12), width=20)
course_menu.place(x=15, y=5)

# Date Selection
Label(root, text="From:", font=('Arial', 14)).place(x=700, y=200)
date_from = DateEntry(root, width=15, font=('Arial', 14), background='darkblue', foreground='white', borderwidth=2)
date_from.place(x=770, y=200)

Label(root, text="To:", font=('Arial', 14)).place(x=700, y=250)
date_to = DateEntry(root, width=15, font=('Arial', 14), background='darkblue', foreground='white', borderwidth=2)
date_to.place(x=770, y=250)

# Table Frame (Treeview)
table_frame = Frame(root, bd=2, relief="ridge")
table_frame.place(x=150, y=400, width=700, height=250)

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

root.mainloop()
