from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
from PIL import ImageTk, Image
import runpy
import sqlite3
from quizdefaults import *

root = Tk()
root.configure(bg="white")
root.attributes("-fullscreen", True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.title("Quiz App - Admin Dashboard")
# root.geometry("900x600")
root.configure(bg=mainframecolor)

# making close and minimize button manually
def min():
    root.iconify()

def on_enter(i):
    btn2['background'] = "red"

def on_leave(i):
    btn2['background'] = "#57a1f8"

def max():
    msg_box = messagebox.askquestion('Exit Application', 'Are you sure you want to close the application?', icon='warning')
    if msg_box == 'yes':
        root.destroy()

label1 = LabelFrame(root, height=35, fg="blue", bg="#57a1f8").place(x=0, y=0)
buttonFont = font.Font(size=14)
btn2 = Button(root, text="✕", command=max, width=4, bg="#57a1f8", border=0, font=buttonFont)
btn2.pack(anchor="ne")
btn2.bind('<Enter>', on_enter)
btn2.bind('<Leave>', on_leave)

btn = Button(root, text="-", command=min, width=4, bg="#57a1f8", border=0, font=buttonFont)
btn.place(x=screen_width-100, y=0)

def enter(i):
    btn['background'] = "red"

def leave(i):
    btn['background'] = "#57a1f8"

btn.bind('<Enter>', enter)
btn.bind('<Leave>', leave)

# Sidebar button functions
def openbutton(btn_text):
    # Clear the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Admin Dashboard
    if btn_text == buttons[0]:
        # Main Dashboard
        header = Label(main_frame, text="Dashboard", font=("Arial", 16, "bold"), bg="#E0E0E0")
        header.pack(pady=10)

        stats_frame = Frame(main_frame, bg="#E0E0E0")
        stats_frame.pack()

        # Stat data
        stat_data = [("123", "Total Users"), ("4", "Total Courses"), ("123", "Total Subcategories"), ("123", "Total Questions")]

        for stat in stat_data:
            stat_box = Frame(stats_frame, bg=buttoncolor, width=120, height=60)
            stat_box.pack_propagate(False)
            stat_box.pack(side=LEFT, padx=10, pady=10)
            
            stat_label = Label(stat_box, text=stat[0], font=("Arial", 14, "bold"), fg="white", bg=buttoncolor)
            stat_label.pack()
            stat_desc = Label(stat_box, text=stat[1], font=("Arial", 10), fg="white", bg=buttoncolor)
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

    # User-Admin Page
    elif btn_text == buttons[1]:
        header = Label(main_frame, text="Users", font=("Arial", 16, "bold"), bg="#E0E0E0")
        header.pack(pady=10)

        stats_frame = Frame(main_frame, bg="#E0E0E0")
        stats_frame.pack()

        pass
    # Courses-Admin Page
    elif btn_text == buttons[2]:
        pass
    # Leaderboard-Admin Page
    elif btn_text == buttons[3]:
        pass
    # Mocktest-Admin Page
    elif btn_text == buttons[4]:
        pass
    # Questions-Admin Page
    elif btn_text == buttons[5]:
        pass
    else:
        label = Label(main_frame, text=btn_text, font=("Arial", 20, "bold"), bg="#E0E0E0")
        label.pack(expand=True)

# Sidebar
sidebar = Frame(root, bg=sidebarcolor, width=200, height=600)
sidebar.pack(side=LEFT, fill=Y)

profile_frame = Frame(sidebar, bg=sidebarcolor)
profile_frame.pack(pady=20)

profile_icon = Label(profile_frame, text="🧑", font=("Arial", 40), bg=sidebarcolor, fg="white")
profile_icon.pack()

profile_name = Label(profile_frame, text="Aayush Bohara", font=("Arial", 12, "bold"), bg=sidebarcolor, fg="white")
profile_name.pack()

edit_profile_btn = Button(profile_frame, text="Edit Profile", bg="#1F618D", fg="white", relief=FLAT, width=15)
edit_profile_btn.pack(pady=5)

# Sidebar buttons
buttons = ["Dashboard", "Users", "Courses", "LeaderBoard", "Mock Test", "Questions"]
for btn_text in buttons:
    sidebarbutton = Button(sidebar, text=btn_text, bg=buttoncolor, fg="white", relief=FLAT, width=20, height=2, command=lambda bt=btn_text: openbutton(bt))
    sidebarbutton.pack(pady=2)

logout_btn = Button(sidebar, text="🔓 LogOut", bg="#E74C3C", fg="white", relief=FLAT, width=20, height=2)
logout_btn.pack(pady=20)

# Main Dashboard
main_frame = Frame(root, bg="#E0E0E0")
main_frame.pack(expand=True, fill=BOTH)

# Initialize with Dashboard
openbutton(buttons[0])

root.mainloop()
