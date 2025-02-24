from tkinter import *
from tkinter import messagebox
import sqlite3

def forgot_pw():
    username_or_email = name_entry.get().strip()
    security_answer = answer_entry.get().strip()
    new_password = newpass_entry.get().strip()
    confirm_password = confirmpass_entry.get().strip()

    # Validation: Check if all fields are filled
    if not username_or_email or not security_answer or not new_password or not confirm_password:
        messagebox.showerror("Error", "All fields are required!")
        return

    # Validation: Check if new password and confirm password match
    if new_password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    # Validation: Check if password length is at least 6 characters
    if len(new_password) < 6:
        messagebox.showerror("Error", "Password must be at least 6 characters long!")
        return

    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()

        # Check if the username or email exists in the database
        c.execute("""
            SELECT user_id, securityquestion, securityanswer 
            FROM users 
            WHERE username = ? OR email = ?
        """, (username_or_email, username_or_email))
        user = c.fetchone()

        if user:
            user_id, security_question, stored_answer = user

            # Check if the security answer matches
            if security_answer == stored_answer:
                # Update the password in the database
                c.execute("""
                    UPDATE users 
                    SET password = ? 
                    WHERE user_id = ?
                """, (new_password, user_id))
                conn.commit()
                messagebox.showinfo("Success", "Password updated successfully!")
                open_login(forgotps)
            else:
                messagebox.showerror("Error", "Incorrect security answer!")
        else:
            messagebox.showerror("Error", "Username or email not found!")

        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def fetch_security_question():
    username_or_email = name_entry.get().strip()

    if not username_or_email:
        messagebox.showerror("Error", "Please enter your username or email!")
        return

    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()

        # Fetch the security question for the given username or email
        c.execute("""
            SELECT securityquestion 
            FROM users 
            WHERE username = ? OR email = ?
        """, (username_or_email, username_or_email))
        result = c.fetchone()

        if result:
            security_question = result[0]
            security_label.config(text=f"Security Question:\n{security_question}")
            answer_entry.config(state=NORMAL)  # Enable the answer entry box
            newpass_entry.config(state=NORMAL)  # Enable the new password entry box
            confirmpass_entry.config(state=NORMAL)  # Enable the confirm password entry box
        else:
            messagebox.showerror("Error", "Username or email not found!")
            security_label.config(text="Security Question:")  # Reset the label
            answer_entry.config(state=DISABLED)  # Disable the answer entry box
            newpass_entry.config(state=DISABLED)  # Disable the new password entry box
            confirmpass_entry.config(state=DISABLED)  # Disable the confirm password entry box

        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI Setup
forgotps = Tk()
forgotps.title("Forgot Password")
forgotps.attributes('-fullscreen', True)

from quizdefaults import *

def adjust_frames(event=None):
    forgotps.update_idletasks()

    window_width = forgotps.winfo_width()
    window_height = forgotps.winfo_height()

    if window_width > 700 or window_height > 400:
        x_main = (window_width - 700) // 2
        y_main = (window_height - 500) // 2
        button_x = window_width - 200
    else:
        x_main, y_main = 0, 0
        button_x = 500

    framemain.place(x=0, y=0, width=window_width, height=window_height)
    topframemain.place(x=0, y=0, width=window_width, height=25)
    welcomeframe.place(x=x_main + 150, y=y_main + 70, width=400, height=600)
    frame.place(x=x_main + 200, y=y_main + 140, width=300, height=450)
    # infotopframe.place(x=x_main + 200, y=y_main + 140, width=300, height=20)
    backframe.place(x=x_main + 450, y=y_main + 140, width=50, height=20)
    register_button.place(x=button_x, y=50)
    login_button.place(x=button_x + 100, y=50)

forgotps.bind("<Configure>", adjust_frames)

# Frame for the main content
framemain = Frame(forgotps, bd=2, relief="ridge", padx=0, pady=0, bg=bgcolor)
framemain.place(x=0, y=0, width=700, height=400)

# Top frame for the header
topframemain = Frame(forgotps, bd=1, relief="ridge", padx=0, pady=0, bg=header_color)
topframemain.place(x=0, y=0, width=700, height=25)
Label(topframemain, text="Quiz App", font=("Arial", 12), padx=20, pady=0, bg=header_color, fg='white').place(x=0, y=0)

# Welcome frame
welcomeframe = Frame(forgotps, bd=2, relief="ridge", padx=0, pady=0, bg=tablecolor)
welcomeframe.place(x=150, y=70, width=400, height=60)
Label(welcomeframe, text="Forgot Password", font=("Arial", 25, "bold"), bg=tablecolor, fg='white').pack(pady=10, padx=10)


# Main frame for input fields
frame = Frame(forgotps, bd=2, relief="ridge", padx=20, pady=20, bg='white')
frame.place(x=200, y=140, width=300, height=300)

# Min and Close buttons
minclose_windowbtn(forgotps)

# Username/Email field
Label(frame, text="Username or Email:", bg='white', fg=label_text_color).place(x=5, y=10)
name_entry = Entry(frame, bg='black', fg='white')
name_entry.place(x=5, y=30)

# Fetch Security Question button
fetch_button = Button(frame, text="Fetch Security Question", command=fetch_security_question, fg='white', bg=button_color)
fetch_button.place(x=5, y=60)

# Security Question label
security_label = Label(frame, text="Security Question:", bg='white', fg=label_text_color)
security_label.place(x=5, y=100)

# Security Answer field
Label(frame, text="Security Answer:", bg='white', fg=label_text_color).place(x=5, y=130)
answer_entry = Entry(frame, bg='black', fg='white', state=DISABLED)  # Disabled until question is fetched
answer_entry.place(x=5, y=150)

# New Password field
Label(frame, text="New Password:", bg='white', fg=label_text_color).place(x=5, y=180)
newpass_entry = Entry(frame, show="*", bg='black', fg='white', state=DISABLED)  # Disabled until question is fetched
newpass_entry.place(x=5, y=200)

# Confirm Password field
Label(frame, text="Confirm Password:", bg='white', fg=label_text_color).place(x=5, y=230)
confirmpass_entry = Entry(frame, show="*", bg='black', fg='white', state=DISABLED)  # Disabled until question is fetched
confirmpass_entry.place(x=5, y=250)

# Update Password button
update_button = Button(frame, text="Update Password", command=forgot_pw, fg='white', bg=button_color)
update_button.place(x=5, y=280)

# Back button
backframe = Frame(forgotps, bd=1, relief="ridge", padx=0, pady=0, bg='black')
backframe.place(x=450, y=140, width=50, height=20)
back_label = Label(backframe, text="Back", bg="black", fg="white", font=("Arial", 10))
back_label.place(x=0, y=0)
back_label.bind("<Button-1>", lambda e: open_login(forgotps))

# Register and Login buttons
register_button = Button(framemain, text="Register", command=lambda: open_registration(forgotps), fg='white', bg=button_color)
register_button.place(x=500, y=30)
login_button = Button(framemain, text="Login", command=lambda: open_login(forgotps), fg='white', bg=button_color)
login_button.place(x=600, y=30)

adjust_frames()

forgotps.mainloop()