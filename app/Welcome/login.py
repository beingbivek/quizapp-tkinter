from tkinter import *
from tkinter import messagebox
import subprocess

'''
# c.execute('SELECT user_id,user_name,password FROM users')
        users = c.fetchall()
        conn.close()
        # for up in users:
        #     if username.get() == up[1]:
                secret = up[2] # put the password variable
                secret = secret.encode('ascii')
                secret = pybase64.b64decode(secret)
                secret = secret.decode('ascii')
        #         if pass.get() == secret:
        #             root.destroy()
        #             runpy.run_path('userdashboard.py')
        #         else:
        #             messagebox.
        #     else:
        #         messagebox
'''

# Colors (matched with Admin panel)
bgcolor = "#ffffff"  # Light gray
header_color = "#003366"  # Deep blue
frame_bg = "#e6e6e6"  # Gray
label_text_color = "#003366"  # Deep blue for text
tablecolor = '#00509e'

def back_to_welcome():
    a.destroy()
    subprocess.Popen(["python", "welcome.py"])

def open_login():
    a.destroy()
    subprocess.Popen(["python", "login.py"])

def open_registration():
    a.destroy()
    subprocess.Popen(["python", "register.py"])

def go_to_forgot():
    a.destroy()
    subprocess.Popen(["python", "forgotps.py"])

def open_admin_login():
    a.destroy()
    subprocess.Popen(["python", "admin.py"])

def login():
    username_or_email = name_entry.get().strip()
    password = user_entry.get().strip()

    if not username_or_email or not password:
        messagebox.showerror("Error", "All fields are required")
        return

    if "@" in username_or_email:
        if "@" not in username_or_email or "." not in username_or_email:
            messagebox.showerror("Error", "Invalid email address")
            return
    else:
        if len(username_or_email) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters long")
            return

    if len(password) < 6:
        messagebox.showerror("Error", "Password must be at least 6 characters long")
        return

    user_info = f"Username/Email: {username_or_email}\nPassword: {'*' * len(password)}"
    messagebox.showinfo("Login Successful", f"Welcome!\n\n{user_info}")

a = Tk()
a.title("Login")
a.attributes('-fullscreen', True)

def adjust_frames(event=None):
    a.update_idletasks()
    window_width = a.winfo_width()
    window_height = a.winfo_height()
    x_main = (window_width - 700) // 2
    y_main = (window_height - 400) // 2
    button_x = window_width - 200
    
    framemain.place(x=0, y=0, width=window_width, height=window_height)
    topframemain.place(x=0, y=0, width=window_width, height=25)
    welcomeframe.place(x=x_main + 150, y=y_main + 70, width=400, height=60)
    frame.place(x=x_main + 200, y=y_main + 140, width=300, height=250)
    infotopframe.place(x=x_main + 200, y=y_main + 140, width=300, height=20)
    backframe.place(x=x_main + 450, y=y_main + 140, width=50, height=20)
    register_button.place(x=button_x, y=30)
    login_button.place(x=button_x + 100, y=30)

a.bind("<Configure>", adjust_frames)

framemain = Frame(a, bd=2, relief="ridge", padx=0, pady=0, bg=bgcolor)
framemain.place(x=0, y=0, width=700, height=400)

topframemain = Frame(a, bd=2, relief="ridge", padx=0, pady=0, bg=header_color)
topframemain.place(x=0, y=0, width=700, height=25)
Label(topframemain, text="Quiz App", font=("Arial", 12), padx=20, pady=0, bg=header_color, fg='white').place(x=0, y=0)

welcomeframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0, bg=tablecolor)
welcomeframe.place(x=150, y=70, width=400, height=60)
Label(welcomeframe, text="Welcome to Quiz App", font=("Arial", 30, "bold"), bg=tablecolor, fg='white').pack(pady=10, padx=10)

frame = Frame(a, bd=2, relief="ridge", padx=20, pady=20, bg=bgcolor)
frame.place(x=200, y=140, width=300, height=250)

Label(frame, text="Email/Username:", bg=bgcolor, fg=label_text_color).place(x=5, y=0)
name_entry = Entry(frame)
name_entry.place(x=5, y=20)

Label(frame, text="Password:", bg=bgcolor, fg=label_text_color).place(x=5, y=50)
user_entry = Entry(frame, show="*")
user_entry.place(x=5, y=70)

Button(frame, text="Forgot Password", command=go_to_forgot, highlightbackground='white').place(x=122, y=110)
Button(frame, text="Admin Login", command=open_admin_login, highlightbackground='white').place(x=156, y=150)
Button(frame, text="Login", command=login, highlightbackground='white').place(x=100, y=190)

infotopframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0, bg=header_color)
infotopframe.place(x=200, y=140, width=300, height=20)
Label(infotopframe, text="Login", font=("Arial", 10), padx=15, pady=-2, bg=header_color, fg='white').place(x=0, y=0)

backframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0, bg='black')
backframe.place(x=450, y=140, width=50, height=20)

back_label = Label(backframe, text="Back", bg="black", fg="white", font=("Arial", 10))
back_label.place(x=0, y=-1)
back_label.bind("<Button-1>", lambda e: back_to_welcome())

register_button = Button(framemain, text="Register", command=open_registration, highlightbackground='white')
register_button.place(x=500, y=30)

login_button = Button(framemain, text="Login", command=open_login, highlightbackground='white')
login_button.place(x=600, y=30)

adjust_frames()
a.mainloop()
