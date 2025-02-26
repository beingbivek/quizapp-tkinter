from tkinter import *
from tkinter import messagebox
import sqlite3

def decrypt_password(encrypted_password):
    try:
        if encrypted_password is None:
            # raise ValueError("No password found in the database.")
            messagebox.showerror('Error','Error in getting password from Database.\nContact the Support.')
        return str_decode(encrypted_password)  # Convert back to the original password
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during decryption: {e}")
        return None

def login():
    username_or_email = name_entry.get()
    password = user_entry.get()

    if not username_or_email or not password:
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE_FILE)  # Replace with your actual database name
        c = conn.cursor()

        # Check if the username or email exists in the database
        c.execute("""
            SELECT * FROM users 
            WHERE username = ? OR email = ?
        """, (username_or_email, username_or_email))
        user = c.fetchone()

        if user:
            # Retrieve the encrypted password from the database
            encrypted_password = user[6]  # Assuming password is the 6th column in the table

            # Decrypt the password
            decrypted_password = decrypt_password(encrypted_password)

            if decrypted_password is None:
                messagebox.showerror("Error", "Failed to decrypt password. Please contact support.")
                return

            # Check if the entered password matches the decrypted password
            if password == decrypted_password:
                messagebox.showinfo("Success", "Login successful!")
                # Writing user ID to a temporary file
                with open(USER_FILE, "w") as f:
                    f.write(",".join(str(data) for data in user))
                open_user_dashboard(user_login)
            else:
                messagebox.showerror("Error", "Incorrect password")
        else:
            messagebox.showerror("Error", "Username or email not found")

        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

user_login = Tk()
user_login.title("Login")
user_login.attributes('-fullscreen', True)

from quizdefaults import *

def adjust_frames(event=None):
    user_login.update_idletasks()
    window_width = user_login.winfo_width()
    window_height = user_login.winfo_height()
    x_main = (window_width - 700) // 2
    y_main = (window_height - 400) // 2
    button_x = window_width - 200
    
    framemain.place(x=0, y=0, width=window_width, height=window_height)
    topframemain.place(x=0, y=0, width=window_width, height=35) #done
    welcomeframe.place(x=x_main + 50, y=y_main - 100, width=500, height=60) #done
    frame.place(x=x_main + 100, y=y_main + 40, width=400, height=400) #done
    infotopframe.place(x=x_main + 100, y=y_main + 25, width=400, height=20)
    backframe.place(x=x_main + 425, y=y_main + 25, width=75, height=20)
    register_button.place(x=button_x, y=50)
    login_button.place(x=button_x + 100, y=50)

user_login.bind("<Configure>", adjust_frames)

framemain = Frame(user_login, bd=2, relief="ridge", padx=0, pady=0, bg=bgcolor)
framemain.place(x=0, y=0, width=700, height=400)

topframemain = Frame(user_login, bd=1, relief="ridge", padx=0, pady=0, bg=header_color)
topframemain.place(x=0, y=0, width=700, height=25)
Label(topframemain, text="Quiz App", font=("Arial", 12), padx=20, pady=0, bg=header_color, fg='white').place(x=0, y=0)

welcomeframe = Frame(user_login, bd=2, relief="ridge", padx=0, pady=0, bg=tablecolor)
welcomeframe.place(x=150, y=70, width=400, height=60)
Label(welcomeframe, text="Welcome to Quiz App", font=("Arial", 25, "bold"), bg=tablecolor, fg='white').pack(pady=10, padx=10)

minclose_windowbtn(user_login)

frame = Frame(user_login, bd=2, relief="ridge", padx=20, pady=20, bg='white')
frame.place(x=200, y=140, width=300, height=250)

Label(frame, text="Email/Username:", bg='white', fg=label_text_color,font=button_font).place(x=5, y=0)
name_entry = Entry(frame, fg='white',font=button_font)
name_entry.place(x=5, y=30)

Label(frame, text="Password:", bg='white', fg=label_text_color,font=button_font).place(x=5, y=60)
user_entry = Entry(frame, show="*", fg='white',font=button_font)
user_entry.place(x=5, y=90)

Button(frame, text="Forgot Password", command=lambda: go_to_forgot(user_login), fg='white', bg=button_color,font=button_font).place(x=180, y=225)
Button(frame, text="Admin Login", command=lambda: open_admin_login(user_login), fg='white', bg=button_color,font=button_font).place(x=5, y=225)
Button(frame, text="Login", command=login, fg='white', bg=button_color,font=button_font).place(x=125, y=150)

infotopframe = Frame(user_login, bd=1, relief="ridge", padx=0, pady=0, bg=header_color)
infotopframe.place(x=200, y=140, width=300, height=20)
Label(infotopframe, text="Login", font=("Arial", 10), padx=15, pady=0, bg=header_color, fg='white').place(x=0, y=0)

backframe = Frame(user_login, bd=1, relief="ridge", padx=0, pady=0, bg='black')
backframe.place(x=450, y=140, width=50, height=20)

back_label = Label(backframe, text="Back", bg="black", fg="white", font=("Arial", 10))
back_label.place(x=0, y=0)
back_label.bind("<Button-1>", lambda e: back_to_welcome(user_login))

register_button = Button(framemain, text="Register", command=lambda: open_registration(user_login), fg='white', bg=button_color,font=button_font)
register_button.place(x=500, y=30)

login_button = Button(framemain, text="Login", command=login, fg='white', bg=button_color,font=button_font)
login_button.place(x=600, y=30)

adjust_frames()
user_login.mainloop()
