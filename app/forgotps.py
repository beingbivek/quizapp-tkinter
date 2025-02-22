from tkinter import *
from tkinter import messagebox
import runpy
import tkinter.font as font

# Colors (matched with Register and Login pages)
bgcolor = "#E0E0E0"  # Background color
header_color = "#34495E"  # Header color
frame_bg = "#E0E0E0"  # Frame background color
button_color = '#1F618D'  # Button color
tablecolor = '#34495E'  # Table color
label_text_color = "black"  # Text color for labels

def back_to_welcome():
    forgotps.destroy()
    runpy.run_path('welcome.py')

def open_login():
    forgotps.destroy()
    runpy.run_path('login.py')

def open_registration():
    forgotps.destroy()
    runpy.run_path('register.py')

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
    register_button.place(x=button_x, y=50)
    login_button.place(x=button_x + 100, y=50)

forgotps.bind("<Configure>", adjust_frames)

framemain = Frame(forgotps, bd=2, relief="ridge", padx=0, pady=0, bg=bgcolor)
framemain.place(x=0, y=0, width=700, height=400)

topframemain = Frame(forgotps, bd=1, relief="ridge", padx=0, pady=0, bg=header_color)
topframemain.place(x=0, y=0, width=700, height=25)
Label(topframemain, text="Quiz App", font=("Arial", 12), padx=20, pady=0, bg=header_color, fg='white').place(x=0, y=0)

welcomeframe = Frame(forgotps, bd=2, relief="ridge", padx=0, pady=0, bg=tablecolor)
welcomeframe.place(x=150, y=70, width=400, height=60)
Label(welcomeframe, text="Welcome to Quiz App", font=("Arial", 25, "bold"), bg=tablecolor, fg='white').pack(pady=10, padx=10)

frame = Frame(forgotps, bd=2, relief="ridge", padx=20, pady=20, bg='white')
frame.place(x=200, y=140, width=300, height=250)

Label(frame, text="Email/Username:", bg='white', fg=label_text_color).place(x=5, y=0)
name_entry = Entry(frame, bg='black', fg='white')
name_entry.place(x=5, y=20)

Label(frame, text="New Password:", bg='white', fg=label_text_color).place(x=5, y=50)
user_entry = Entry(frame, show="*", bg='black', fg='white')
user_entry.place(x=5, y=70)

Button(frame, text="Update", command=forgot_pw, fg='white', bg=button_color).place(x=100, y=190)

infotopframe = Frame(forgotps, bd=1, relief="ridge", padx=0, pady=0, bg=header_color)
infotopframe.place(x=200, y=140, width=300, height=20)
Label(infotopframe, text="Forgot Password", font=("Arial", 10), padx=15, pady=0, bg=header_color, fg='white').place(x=0, y=0)

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
    forgotps.iconify()

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
        forgotps.destroy()

btn2 = Button(topframemain, text="✕", command=max, width=4, bg=HEADER_COLOR, border=1, font=button_font)
btn2.place(x=1125,y=-5)
btn2.bind('<Enter>', on_enter)
btn2.bind('<Leave>', on_leave)

btn = Button(topframemain, text="-", command=min, width=4, bg=HEADER_COLOR, border=1, font=button_font)
btn.place(x=1175,y=-5)
btn.bind('<Enter>', enter)
btn.bind('<Leave>', leave)

backframe = Frame(forgotps, bd=1, relief="ridge", padx=0, pady=0, bg='black')
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

register_button = Button(framemain, text="Register", command=open_registration, fg='white', bg=button_color)
register_button.place(x=500, y=30)

login_button = Button(framemain, text="Login", command=open_login, fg='white', bg=button_color)
login_button.place(x=600, y=30)

adjust_frames()
forgotps.mainloop()