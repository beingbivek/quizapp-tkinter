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
    admin_login.destroy()
    subprocess.Popen(["python", "welcome.py"])

def open_login():
    admin_login.destroy()
    subprocess.Popen(["python", "login.py"])

def open_registration():
    admin_login.destroy()
    subprocess.Popen(["python", "register.py"])

def admin_login_function():
    entered_code = admin_code_entry.get().strip()

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

topframemain = Frame(admin_login, bd=2, relief="ridge", padx=0, pady=0, bg='#003366')
topframemain.place(x=0, y=0, width=700, height=25)
Label(topframemain, text="Quiz App", font=("Arial", 12), padx=20, pady=0, bg='#003366').place(x=0, y=0)

welcomeframe = Frame(admin_login, bd=2, relief="ridge", padx=0, pady=0, bg=tablecolor)
welcomeframe.place(x=150, y=70, width=400, height=60)
Label(welcomeframe, text="Welcome to Quiz App", font=("Arial", 25, "bold"), bg=tablecolor).pack(pady=10, padx=10)

frame = Frame(admin_login, bd=2, relief="ridge", padx=20, pady=20, bg=bgcolor)
frame.place(x=200, y=140, width=300, height=250)

Label(frame, text="Enter Admin Code:",bg='white',fg='black').place(x=5, y=0)
admin_code_entry = Entry(frame, show="*")
admin_code_entry.place(x=5, y=20)

Button(frame, text="Login", command=admin_login_function,highlightbackground='white').place(x=100, y=190)

infotopframe = Frame(admin_login, bd=2, relief="ridge", padx=0, pady=0, bg='#003366')
infotopframe.place(x=200, y=140, width=300, height=20)
Label(infotopframe, text="Admin Login", font=("Arial", 10), padx=15, pady=-2, bg='#003366').place(x=0, y=0)

backframe = Frame(admin_login, bd=2, relief="ridge", padx=0, pady=0, bg='black')
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
admin_login.mainloop()