from tkinter import *
from tkinter import messagebox
import runpy
import tkinter.font as font

# Colors (matched with Register page)
bgcolor = "#E0E0E0"  # Background color
header_color = "#34495E"  # Header color
frame_bg = "#E0E0E0"  # Frame background color
button_color = '#1F618D'  # Button color
tablecolor = '#34495E'  # Table color
label_text_color = "black"  # Text color for labels

# Predefined admin code (change this as needed)
ADMIN_CODE = "12345"

def back_to_welcome():
    admin_login.destroy()
    runpy.run_path(r'..\quizapp-tkinter\app\welcome.py')

def open_login():
    admin_login.destroy()
    runpy.run_path(r'..\quizapp-tkinter\app\login.py')

def open_registration():
    admin_login.destroy()
    runpy.run_path(r'..\quizapp-tkinter\app\register.py')

def admin_login_function():
    entered_code = admin_code_entry.get().strip()
    messagebox.showinfo("Success", "Login successful!")
    runpy.run_path(r'..\quizapp-tkinter\app\admindashboard.py')

    if not entered_code:
        messagebox.showerror("Error", "Admin code is required")
        return

    if entered_code == ADMIN_CODE:
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
    else:
        messagebox.showerror("Error", "Invalid admin code")

admin_login = Tk()
admin_login.title("Admin Login")
admin_login.attributes('-fullscreen', True)

def adjust_frames(event=None):
    admin_login.update_idletasks()

    window_width = admin_login.winfo_width()
    window_height = admin_login.winfo_height()

    if window_width > 700 or window_height > 400:
        x_main = (window_width - 700) // 2
        y_main = (window_height - 400) // 2
        button_x = window_width - 200
    else:
        x_main, y_main = 0, 0
        button_x = 500

    framemain.place(x=0, y=0, width=window_width, height=window_height)
    topframemain.place(x=0, y=0, width=window_width, height=25)
    welcomeframe.place(x=x_main + 150, y=y_main + 70, width=400, height=60)
    frame.place(x=x_main + 200, y=y_main + 140, width=300, height=250)
    infotopframe.place(x=x_main + 200, y=y_main + 140, width=300, height=20)
    backframe.place(x=x_main + 450, y=y_main + 140, width=50, height=20)
    register_button.place(x=button_x, y=50)
    login_button.place(x=button_x + 100, y=50)

admin_login.bind("<Configure>", adjust_frames)

framemain = Frame(admin_login, bd=2, relief="ridge", padx=0, pady=0, bg=bgcolor)
framemain.place(x=0, y=0, width=700, height=400)

topframemain = Frame(admin_login, bd=1, relief="ridge", padx=0, pady=0, bg=header_color)
topframemain.place(x=0, y=0, width=700, height=25)
Label(topframemain, text="Quiz App", font=("Arial", 12), padx=20, pady=0, bg=header_color, fg='white').place(x=0, y=0)

welcomeframe = Frame(admin_login, bd=2, relief="ridge", padx=0, pady=0, bg=tablecolor)
welcomeframe.place(x=150, y=70, width=400, height=60)
Label(welcomeframe, text="Welcome to Quiz App", font=("Arial", 25, "bold"), bg=tablecolor, fg='white').pack(pady=10, padx=10)

frame = Frame(admin_login, bd=2, relief="ridge", padx=20, pady=20, bg='white')
frame.place(x=200, y=140, width=300, height=250)

Label(frame, text="Enter Admin Code:", bg='white', fg=label_text_color).place(x=5, y=0)
admin_code_entry = Entry(frame, show="*", bg='black', fg='white')
admin_code_entry.place(x=5, y=20)

Button(frame, text="Login", command=admin_login_function, fg='white', bg=button_color).place(x=100, y=190)

infotopframe = Frame(admin_login, bd=1, relief="ridge", padx=0, pady=0, bg=header_color)
infotopframe.place(x=200, y=140, width=300, height=20)
Label(infotopframe, text="Admin Login", font=("Arial", 10), padx=15, pady=0, bg=header_color, fg='white').place(x=0, y=0)

# Making close and minimize button manually
MAINFRAME_COLOR = "#E0E0E0"
SIDEBAR_COLOR = "#2C3E50"
BUTTON_COLOR = "#34495E"
HIGHLIGHT_COLOR = "#1A252F"
HEADER_COLOR = "#57a1f8"
PROFILE_COLOR = "#1F618D"
LOGOUT_COLOR = "#E74C3C"
FG_COLOR = "white"
button_font = font.Font(size=14)

def min():
    admin_login.iconify()

def on_enter(i):
    btn2['background'] = "red"

def on_leave(i):
    btn2['background'] = HEADER_COLOR

def enter(i):
    btn['background'] = "red"

def leave(i):
    btn['background'] = HEADER_COLOR

def max():
    msg_box = messagebox.askquestion('Exit Application', 'Are you sure you want to close the application?', icon='warning')
    if msg_box == 'yes':
        admin_login.destroy()

btn2 = Button(topframemain, text="✕", command=max, width=4, bg=HEADER_COLOR, border=1, font=button_font)
btn2.place(x=1230,y=-5)
btn2.bind('<Enter>', on_enter)
btn2.bind('<Leave>', on_leave)

btn = Button(topframemain, text="-", command=min, width=4, bg=HEADER_COLOR, border=1, font=button_font)
btn.place(x=1180,y=-5)
btn.bind('<Enter>', enter)
btn.bind('<Leave>', leave)

backframe = Frame(admin_login, bd=1, relief="ridge", padx=0, pady=0, bg='black')
backframe.place(x=450, y=140, width=50, height=20)

# Use Label as a button
back_label = Label(
    backframe,
    text="Back",
    bg="black",
    fg="white",
    font=("Arial", 10),
)
back_label.place(x=0, y=0)

# Bind a click event to the label
back_label.bind("<Button-1>", lambda e: open_login())

# Top buttons
register_button = Button(framemain, text="Register", command=open_registration, fg='white', bg=button_color)
register_button.place(x=500, y=30)

login_button = Button(framemain, text="Login", command=open_login, fg='white', bg=button_color)
login_button.place(x=600, y=30)

adjust_frames()
admin_login.mainloop()