import tkinter as tk
from tkinter import ttk

# Create main window
root = tk.Tk()
root.title("Quiz App - User Dashboard")
root.geometry("900x600")
root.configure(bg='white')

# Sidebar Frame
sidebar = tk.Frame(root, bg='#2C3E50', width=200, height=600)
sidebar.pack(side='left', fill='y')

# Profile Image Placeholder
profile_img = tk.Label(sidebar, text="Profile Image", bg='white', width=15, height=5)
profile_img.pack(pady=10)

# Username and Score
username_label = tk.Label(sidebar, text="Aayush Bohara", fg='white', bg='#2C3E50', font=("Arial", 12, "bold"))
username_label.pack()

score_label = tk.Label(sidebar, text="Score: 1500", fg='white', bg='#2C3E50', font=("Arial", 10))
score_label.pack()

# Sidebar Buttons
def sidebar_button(text):
    return tk.Button(sidebar, text=text, bg='#34495E', fg='white', font=("Arial", 10, "bold"), width=20, height=2, bd=0)

tk.Button(sidebar, text="Dashboard", bg='#1A252F', fg='white', font=("Arial", 10, "bold"), width=20, height=2, bd=0).pack()
sidebar_button("Courses").pack()
sidebar_button("LeaderBoard").pack()
sidebar_button("Mock Test").pack()
sidebar_button("About US").pack()

# Logout Button
logout_btn = tk.Button(sidebar, text="Logout", bg='#E74C3C', fg='white', font=("Arial", 10, "bold"), width=20, height=2, bd=0)
logout_btn.pack(side='bottom', pady=20)

# Main Content Frame
main_content = tk.Frame(root, bg='white', padx=20, pady=20)
main_content.pack(expand=True, fill='both')

# Question of the Day
qotd_label = tk.Label(main_content, text="Question of the day!", font=("Arial", 16, "bold"), bg='white')
qotd_label.pack(anchor='w')

topic_label = tk.Label(main_content, text="Topic: Loksewa/Animal", font=("Arial", 12), bg='white')
topic_label.pack(anchor='w')

question_label = tk.Label(main_content, text="Q. How fast can a Cheetah run?", font=("Arial", 12), bg='white')
question_label.pack(anchor='w')

options = ["80 kmph", "90 Kmph", "100 Kmph", "120 Kmph"]
selected_option = tk.StringVar()
selected_option.set(None)

for opt in options:
    tk.Radiobutton(main_content, text=opt, variable=selected_option, value=opt, bg='white').pack(anchor='w')

# Progress Table
progress_label = tk.Label(main_content, text="Your Progress", font=("Arial", 14, "bold"), bg='white')
progress_label.pack(anchor='w', pady=10)

columns = ("SN", "Courses", "Tackled", "Correct", "Incorrect")
progress_table = ttk.Treeview(main_content, columns=columns, show='headings', height=4)

for col in columns:
    progress_table.heading(col, text=col)
    progress_table.column(col, width=100, anchor='center')

progress_data = [(1, "CEE", 40, 30, 10), (2, "IOE", 38, 8, 30), (3, "Driving", 41, 1, 40), (4, "LokSewa", 45, 40, 5)]
for row in progress_data:
    progress_table.insert('', tk.END, values=row)
progress_table.pack()

# Mock Test Results Table
mock_label = tk.Label(main_content, text="Previous Mock Test Results", font=("Arial", 14, "bold"), bg='white')
mock_label.pack(anchor='w', pady=10)

mock_columns = ("SN", "Mock TestID", "Datetime", "Course", "Result")
mock_table = ttk.Treeview(main_content, columns=mock_columns, show='headings', height=4)

for col in mock_columns:
    mock_table.heading(col, text=col)
    mock_table.column(col, width=120, anchor='center')

mock_data = [(1, "CEE12", "2024/5/20 15:20", "CEE", "50/100"),
             (2, "IOE312", "2024/5/20 15:20", "IOE", "50/100"),
             (3, "Driving123", "2024/5/20 15:20", "Driving", "50/100"),
             (4, "LokSewa4334", "2024/5/20 15:20", "Loksewa", "50/100")]

for row in mock_data:
    mock_table.insert('', tk.END, values=row)
mock_table.pack()

root.mainloop()
