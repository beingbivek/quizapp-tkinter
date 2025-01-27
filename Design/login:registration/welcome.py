from tkinter import *
import subprocess

a = Tk()
a.title("Quiz App")
a.geometry('700x400')
a.resizable(1, 1)


def open_registration():
    a.destroy()
    subprocess.Popen(["python", "register.py"])

def open_login():
    a.destroy()
    subprocess.Popen(["python", "login.py"])


# Function to center frames dynamically
def center_frames(event=None):
    a.update_idletasks()
    
    window_width = a.winfo_width()
    window_height = a.winfo_height()
    
    frame_width = 700
    frame_height = 400
    message_width = 500
    message_height = 250
    welcome_width = 400
    welcome_height = 60

    # Calculate center positions
    x_main = (window_width - frame_width) // 2
    y_main = (window_height - frame_height) // 2

    x_message = (window_width - message_width) // 2
    y_message = y_main + 140

    x_welcome = (window_width - welcome_width) // 2
    y_welcome = y_main + 70

    # Adjust frame positions
    framemain.place(x=x_main, y=y_main, width=700, height=400)
    topframemain.place(x=x_main, y=y_main, width=700, height=25)
    welcomeframe.place(x=x_welcome, y=y_welcome, width=400, height=60)
    frame.place(x=x_message, y=y_message, width=500, height=250)

# Main frame
framemain = Frame(a, bd=2, relief="ridge", padx=0, pady=0)
framemain.place(x=0, y=0, width=700, height=400)

# Top frame with title
topframemain = Frame(a, bd=2, relief="ridge", padx=0, pady=0)
Label(topframemain, text="Quiz App", font=("Arial", 12), padx=20, pady=0).place(x=0, y=0)

# Welcome frame
welcomeframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0)
Label(welcomeframe, text="Welcome to Quiz App", font=("Arial", 30, "bold")).pack(pady=10, padx=10)

# Welcome message frame
frame = Frame(a, bd=2, relief="ridge", padx=20, pady=20)
Label(frame, text='''
Get ready to explore a world of knowledge and sharpen your skills with ease. 
Our app offers a variety of tests and practice questions tailored for:

CEE (Common Entrance Exam)
Loksewa (Public Service Commission)
Driving License Preparation
IOE (Institute of Engineering)

Whether you're preparing for competitive exams or brushing up your knowledge,
Quiz App is here to help you succeed. Start your journey today!
''', font=("Arial", 13)).place(x=-10, y=0)

# Buttons
Button(framemain, text="Register", command=open_registration).place(x=500, y=30)
Button(framemain, text="Login", command=open_login).place(x=600, y=30)

Button(frame, text="Register", command=open_registration).place(x=0, y=190)
Button(frame, text="Login", command=open_login).place(x=390, y=190)

# Bind the resize event to reposition elements dynamically
a.bind("<Configure>", center_frames)

# Call the function initially to center elements at startup
center_frames()

a.mainloop()
