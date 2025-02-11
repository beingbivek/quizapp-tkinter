from tkinter import *
import subprocess

# Colors
bgcolor = "#ffffff"  # Light gray
header_color = "#003366"  # Deep blue
frame_bg = "#e6e6e6"  # Gray
label_text_color = "#003366"  # Deep blue for text
tablecolor= '#00509e'

a = Tk()
a.title("Quiz App")
a.attributes('-fullscreen', True)

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

    if window_width > 700 or window_height > 400:
        x_main = (window_width - 700) // 2
        y_main = (window_height - 400) // 2
        button_x = window_width - 200
    else:
        x_main, y_main = 0, 0
        button_x = 500

    # Calculate center positions
    x_main = (window_width - frame_width) // 2
    y_main = (window_height - frame_height) // 2

    x_message = (window_width - message_width) // 2
    y_message = y_main + 140

    x_welcome = (window_width - welcome_width) // 2
    y_welcome = y_main + 70

    # Adjust frame positions
    framemain.place(x=0, y=0, width=window_width, height=window_height)
    topframemain.place(x=0, y=0, width=window_width, height=25)
    welcomeframe.place(x=x_welcome, y=y_welcome, width=400, height=60)
    frame.place(x=x_message, y=y_message, width=500, height=250)
    register_button.place(x=button_x, y=30)
    login_button.place(x=button_x + 100, y=30)

# Main frame
framemain = Frame(a, bd=2, relief="ridge", padx=0, pady=0, bg=bgcolor)
framemain.place(x=0, y=0, width=700, height=400)

# Top frame with title
topframemain = Frame(a, bd=2, relief="ridge", padx=0, pady=0, bg=header_color)
topframemain.place(x=0, y=0, width=700, height=25)
Label(topframemain, text="Quiz App", font=("Arial", 12), padx=20, pady=0, bg=header_color, fg="white").place(x=0, y=0)

# Welcome frame
welcomeframe = Frame(a, bd=2, relief="ridge", padx=0, pady=0, bg=tablecolor)
welcomeframe.place(x=150, y=70, width=400, height=60)
Label(welcomeframe, text="Welcome to Quiz App", font=("Arial", 30, "bold"), bg=tablecolor, fg="white").pack(pady=10, padx=10)

# Welcome message frame
frame = Frame(a, bd=2, relief="ridge", padx=20, pady=20, bg=bgcolor)
Label(frame, text='''
Get ready to explore a world of knowledge and sharpen your skills with ease. 
Our app offers a variety of tests and practice questions tailored for:

CEE (Common Entrance Exam)
Loksewa (Public Service Commission)
Driving License Preparation
IOE (Institute of Engineering)

Whether you're preparing for competitive exams or brushing up your knowledge,
Quiz App is here to help you succeed. Start your journey today!
''', font=("Arial", 13), bg=bgcolor,fg='black').place(x=-10, y=0)

# Buttons
Button(frame, text="Register", command=open_registration, highlightbackground='white').place(x=0, y=190)
Button(frame, text="Login", command=open_login, highlightbackground='white').place(x=390, y=190)

# Top buttons
register_button = Button(framemain, text="Register", command=open_registration,highlightbackground='white')
register_button.place(x=500, y=30)

login_button = Button(framemain, text="Login", command=open_login,highlightbackground='white')
login_button.place(x=600, y=30)

# Bind the resize event to reposition elements dynamically
a.bind("<Configure>", center_frames)

# Call the function initially to center elements at startup
center_frames()

a.mainloop()
