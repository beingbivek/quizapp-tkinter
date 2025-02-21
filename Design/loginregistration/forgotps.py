from tkinter import *
from tkinter import messagebox
import subprocess

# Colors
bgcolor = "#ffffff"  # Light gray
header_color = "#003366"  # Deep blue
frame_bg = "#e6e6e6"  # Gray
label_text_color = "#003366"  # Deep blue for text
tablecolor= '#00509e'


def back_to_welcome():
    forgotps.destroy()
    subprocess.Popen(["python", "welcome.py"])

def open_login():
    forgotps.destroy()
    subprocess.Popen(["python", "login.py"])

def open_registration():
    forgotps.destroy()
    subprocess.Popen(["python", "register.py"])

def forgot_pw():
    username_or_email = name_entry.get().strip()
    newpassword = user_entry.get().strip()

    if not username_or_email or not newpassword:
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

    if len(newpassword) < 6:
        messagebox.showerror("Error", "Password must be at least 6 characters long")
        return

    # Show success message with user details (masking password)
    user_info = f"Username/Email: {username_or_email}\nNew Password: {'*' * len(newpassword)}"
    messagebox.showinfo("Success", f"Password updated successfully!\n\n{user_info}")

forgotps = Tk()
forgotps.title("Forgot Password")
forgotps.attributes('-fullscreen', True)

def adjust_frames(event=None):
    forgotps.update_idletasks()

    window_width = forgotps.winfo_width()
    window_height = forgotps.winfo_height()

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
    register_button.place(x=button_x, y=30)
    login_button.place(x=button_x + 100, y=30)

forgotps.bind("<Configure>", adjust_frames)

framemain = Frame(forgotps, bd=2, relief="ridge", padx=0, pady=0,bg=bgcolor)
framemain.place(x=0, y=0, width=700, height=400)

topframemain = Frame(forgotps, bd=2, relief="ridge", padx=0, pady=0, bg='#003366')
topframemain.place(x=0, y=0, width=700, height=25)
Label(topframemain, text="Quiz App", font=("Arial", 12), padx=20, pady=0, bg='#003366').place(x=0, y=0)

welcomeframe = Frame(forgotps, bd=2, relief="ridge", padx=0, pady=0, bg=tablecolor)
welcomeframe.place(x=150, y=70, width=400, height=60)
Label(welcomeframe, text="Welcome to Quiz App", font=("Arial", 25, "bold"), bg=tablecolor).pack(pady=10, padx=10)

frame = Frame(forgotps, bd=2, relief="ridge", padx=20, pady=20, bg=bgcolor)
frame.place(x=200, y=140, width=300, height=250)

Label(frame, text="Email/Username:",bg='white',fg='black').place(x=5, y=0)
name_entry = Entry(frame)
name_entry.place(x=5, y=20)

Label(frame, text="New Password:",bg='white',fg='black').place(x=5, y=50)
user_entry = Entry(frame, show="*")
user_entry.place(x=5, y=70)

Button(frame, text="Update", command=forgot_pw,highlightbackground='white').place(x=100, y=190)

infotopframe = Frame(forgotps, bd=2, relief="ridge", padx=0, pady=0, bg='#003366')
infotopframe.place(x=200, y=140, width=300, height=20)
Label(infotopframe, text="Forgot Password", font=("Arial", 10), padx=15, pady=-2, bg='#003366').place(x=0, y=0)

backframe = Frame(forgotps, bd=2, relief="ridge", padx=0, pady=0, bg='black')
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

register_button = Button(framemain, text="Register", command=open_registration,highlightbackground='white')
register_button.place(x=500, y=30)

login_button = Button(framemain, text="Login", command=open_login,highlightbackground='white')
login_button.place(x=600, y=30)

adjust_frames()
forgotps.mainloop()
