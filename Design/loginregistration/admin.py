from tkinter import *
from tkinter import messagebox
import subprocess

# Colors
bgcolor = "#ffffff"  # Light gray
header_color = "#003366"  # Deep blue
frame_bg = "#e6e6e6"  # Gray
label_text_color = "#003366"  # Deep blue for text
tablecolor= '#00509e'

# Predefined admin code (change this as needed)
ADMIN_CODE = "12345"

def back_to_welcome():
    a.destroy()
    subprocess.Popen(["python", "welcome.py"])

def open_login():
    a.destroy()
    subprocess.Popen(["python", "login.py"])

def open_registration():
    a.destroy()
    subprocess.Popen(["python", "register.py"])

def admin_login():
    entered_code = admin_code_entry.get().strip()

    if not entered_code:
        messagebox.showerror("Error", "Admin code is required")
        return

    if entered_code == ADMIN_CODE:
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
    else:
        messagebox.showerror("Error", "Invalid admin code")

a = Tk()
a.title("Admin Login")
a.geometry('700x400')
a.resizable(1, 1)

def adjust_frames(event=None):
    a.update_idletasks()

    window_width = a.winfo_width()
    window_height = a.winfo_height()

    if window_width > 700 or window_height > 400:
        x_main = (window_width - 700) // 2
        y_main = (window_height - 400) // 2
        button_x = window_width - 200
    else:
        x_main, y_main = 0, 0
        button_x = 500

    framemain.place(x=0, y=0, width=2560, height=1600)
    topframemain.place(x=0, y=0, width=2560, height=25)
    welcomeframe.place(x=x_main + 150, y=y_main + 70, width=400, height=60)
    frame.place(x=x_main + 200, y=y_main + 140, width=300, height=250)
    infotopframe.place(x=x_main + 200, y=y_main + 140, width=300, height=20)
    backframe.place(x=x_main + 450, y=y_main + 140, width=50, height=20)
    register_button.place(x=button_x, y=30)
    login_button.place(x=button_x + 100, y=30)

a.bind("<Configure>", adjust_frames)

framemain = Frame(a, bd=2, relief="ridge", padx=0, pady=0, bg=bgcolor)
framemain.place(x=0, y=0, width=700, height=400)

topframemain = Frame(a, bd=2, relief="ridge", padx=0, pady=0, bg='#003366')
topframemain.place(x=0, y=0, width=700, height=25)
Label(topframemain, text="Quiz App", font=("Arial", 12), padx=20, pady=0, bg='#003366').place(x=0, y=0)

welcomeframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0, bg=tablecolor)
welcomeframe.place(x=150, y=70, width=400, height=60)
Label(welcomeframe, text="Welcome to Quiz App", font=("Arial", 30, "bold"), bg=tablecolor).pack(pady=10, padx=10)

frame = Frame(a, bd=2, relief="ridge", padx=20, pady=20, bg=bgcolor)
frame.place(x=200, y=140, width=300, height=250)

Label(frame, text="Enter Admin Code:",bg='white',fg='black').place(x=5, y=0)
admin_code_entry = Entry(frame, show="*")
admin_code_entry.place(x=5, y=20)

Button(frame, text="Login", command=admin_login,highlightbackground='white').place(x=100, y=190)

infotopframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0, bg='#003366')
infotopframe.place(x=200, y=140, width=300, height=20)
Label(infotopframe, text="Admin Login", font=("Arial", 10), padx=15, pady=-2, bg='#003366').place(x=0, y=0)

backframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0, bg='black')
backframe.place(x=450, y=140, width=50, height=20)

# Use Label as a button
back_label = Label(
    backframe,
    text="Back",
    bg="black",
    fg="white",
    font=("Arial", 10),
)
back_label.place(x=0, y=-1)

# Bind a click event to the label
back_label.bind("<Button-1>", lambda e : open_login())


# Top buttons
register_button = Button(framemain, text="Register", command=open_registration,highlightbackground='white')
register_button.place(x=500, y=30)

login_button = Button(framemain, text="Login", command=open_login,highlightbackground='white')
login_button.place(x=600, y=30)

adjust_frames()
a.mainloop()
