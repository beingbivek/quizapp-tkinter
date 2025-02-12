from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Colors
bgcolor = "#E0E0E0"
sidebar_color = "#2C3E50"
button_color = "#34495E"
accent_color = "#1F618D"
delete_color = "#E74C3C"

# Create main window
a = Tk()
a.title("Quiz App - Admin Dashboard")
a.geometry("900x600")
a.configure(bg=bgcolor)

# Sidebar
sidebar = Frame(a, bg=sidebar_color)
sidebar.place(relx=0, rely=0, relwidth=0.2, relheight=1)

# Profile section
profile_frame = Frame(sidebar, bg=sidebar_color)
profile_frame.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.2)

profile_icon = Label(profile_frame, text="🧑", font=("Arial", 40), bg=sidebar_color, fg="black")
profile_icon.place(relx=0.5, rely=0.2, anchor=CENTER)

profile_name = Label(profile_frame, text="Aayush Bohara", font=("Arial", 12, "bold"), bg=sidebar_color, fg="white")
profile_name.place(relx=0.5, rely=0.6, anchor=CENTER)

edit_profile_btn = Button(profile_frame, text="Edit Profile", bg=accent_color, fg="black", relief=FLAT, width=15)
edit_profile_btn.place(relx=0.5, rely=0.8, anchor=CENTER)

# Sidebar buttons
buttons = ["Dashboard", "Users", "Courses", "LeaderBoard", "Mock Test", "Questions"]
y_offset = 0.3
for btn_text in buttons:
    btn = Button(sidebar, text=btn_text, bg=button_color, fg="black", relief=FLAT)
    btn.place(relx=0.1, rely=y_offset, relwidth=0.8, relheight=0.07)
    y_offset += 0.09

logout_btn = Button(sidebar, text="🔓 LogOut", bg=delete_color, fg="black", relief=FLAT)
logout_btn.place(relx=0.1, rely=0.85, relwidth=0.8, relheight=0.07)

# Main Dashboard
main_frame = Frame(a, bg=bgcolor)
main_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)

header = Label(main_frame, text="Dashboard", font=("Arial", 16, "bold"), bg=bgcolor)
header.place(relx=0.05, rely=0.02)

# Stats section
stats_frame = Frame(main_frame, bg=bgcolor)
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
search_label = Label(main_frame, text="Search:", font=("Arial", 13), bg=bgcolor, fg='black')
search_label.place(relx=0.45, rely=0.25)

search_entry = Entry(main_frame, font=("Arial", 10), width=20)
search_entry.place(relx=0.52, rely=0.25)

search_button = Button(main_frame, text="Search", bg=accent_color, fg="black", relief=FLAT, command=lambda: search_table())
search_button.place(relx=0.72, rely=0.25, width=80)

# Table
table_frame = Frame(main_frame, bg=bgcolor)
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
    register_window = Toplevel(a)
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
    edit_window = Toplevel(a)
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


a.mainloop()