import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Quiz App - Admin Dashboard")

# Create a main frame
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Header Section
header_label = ttk.Label(main_frame, text="Quiz App", font=("Arial", 16))
header_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

author_label = ttk.Label(main_frame, text="Aayush Bohara", font=("Arial", 12))
author_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))

# Navigation Section
nav_frame = ttk.Frame(main_frame)
nav_frame.grid(row=2, column=0, sticky=tk.W, pady=(0, 10))

edit_profile_btn = ttk.Button(nav_frame, text="Edit Profile")
edit_profile_btn.grid(row=0, column=0, padx=(0, 10))

dashboard_btn = ttk.Button(nav_frame, text="Dashboard")
dashboard_btn.grid(row=0, column=1, padx=(0, 10))

# Dashboard Section
dashboard_frame = ttk.Frame(main_frame)
dashboard_frame.grid(row=3, column=0, sticky=tk.W)

# Task Overview Section
task_overview_label = ttk.Label(dashboard_frame, text="Task Overview", font=("Arial", 14))
task_overview_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

# Total Users
total_users_frame = ttk.Frame(dashboard_frame)
total_users_frame.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))

total_users_label = ttk.Label(total_users_frame, text="Total Users: 123")
total_users_label.grid(row=0, column=0)

total_courses_label = ttk.Label(total_users_frame, text="Total Courses: 4")
total_courses_label.grid(row=1, column=0)

# Total Subcategories and Questions
total_subcategories_frame = ttk.Frame(dashboard_frame)
total_subcategories_frame.grid(row=2, column=0, sticky=tk.W, pady=(0, 10))

total_subcategories_label = ttk.Label(total_subcategories_frame, text="Total Subcategories: 123")
total_subcategories_label.grid(row=0, column=0)

total_questions_label = ttk.Label(total_subcategories_frame, text="Total Questions: 123")
total_questions_label.grid(row=1, column=0)

# Particulars
particulars_frame = ttk.Frame(dashboard_frame)
particulars_frame.grid(row=3, column=0, sticky=tk.W, pady=(0, 10))

particulars_label = ttk.Label(particulars_frame, text="Particulars: Numbers - Remark")
particulars_label.grid(row=0, column=0)

# User Registered Today
user_registered_frame = ttk.Frame(dashboard_frame)
user_registered_frame.grid(row=4, column=0, sticky=tk.W, pady=(0, 10))

user_registered_label = ttk.Label(user_registered_frame, text="User Registered Today: 56 (Grown by 10%)")
user_registered_label.grid(row=0, column=0)

# Mock Test Today
mock_test_frame = ttk.Frame(dashboard_frame)
mock_test_frame.grid(row=5, column=0, sticky=tk.W, pady=(0, 10))

mock_test_label = ttk.Label(mock_test_frame, text="Mock Test Today: 50 (Grown by 10%)")
mock_test_label.grid(row=0, column=0)

# Run the application
root.mainloop()