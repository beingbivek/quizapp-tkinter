import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import Tk
root = Tk()
from quizdefaults import *

# Database connection
# DATABASE_FILE = "quiz.db"
LOGGED_IN_USER = [1]  # Example: Replace with your actual logged-in user ID

# Fetch leaderboard data
def fetch_leaderboard_data(logged_in_user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    query = """
        SELECT 
            c.coursename, 
            u.user_id, 
            u.username, 
            SUM(mr.result) AS total_score
        FROM mocktestresults mr
        JOIN users u ON mr.user_id = u.user_id
        JOIN courses c ON mr.course_id = c.course_id
        GROUP BY c.coursename, u.user_id
        ORDER BY c.coursename, total_score DESC;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    leaderboard_data = {}
    user_positions = {}

    for course, user_id, username, total_score in results:
        if course not in leaderboard_data:
            leaderboard_data[course] = []
        leaderboard_data[course].append([len(leaderboard_data[course]) + 1, username, total_score])

        # Store the position of the logged-in user
        if user_id == logged_in_user_id:
            user_positions[course] = len(leaderboard_data[course])

    # Filter data: Top 5 + logged-in user (if they are outside top 5)
    filtered_data = {}
    for course, users in leaderboard_data.items():
        top_5 = users[:5]  # Get top 5 users

        if course in user_positions and user_positions[course] > 5:
            # Find logged-in user's data
            logged_user_data = next((x for x in users if x[1] == logged_in_user_id), None)
            if logged_user_data:
                logged_user_data = [user_positions[course]] + logged_user_data[1:]  # Update with actual position
                top_5.append(logged_user_data)

        filtered_data[course] = top_5

    return filtered_data

# Create a scrollable table using Treeview
def create_table(frame, data, course_name):
    # Course title
    title_label = tk.Label(frame, text=course_name, font=("Arial", 14, "bold"), fg="black", bg="#E74C3C")
    title_label.pack(pady=5)

    # Create a Treeview widget
    tree = ttk.Treeview(frame, columns=("SN", "Username", "Score"), show="headings")
    tree.heading("SN", text="SN")
    tree.heading("Username", text="Username")
    tree.heading("Score", text="Score")
    tree.column("SN", width=50, anchor="center")
    tree.column("Username", width=150, anchor="center")
    tree.column("Score", width=100, anchor="center")

    # Insert data into the Treeview
    for row in data:
        tree.insert("", "end", values=row)

    # Add a vertical scrollbar for the table
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

# Main application
def create_leaderboard(main_frame):
    # Header
    header = tk.Label(main_frame, text="Leaderboard", font=("Arial", 16, "bold"), bg="white")
    header.pack(pady=10)

    # Fetch leaderboard data
    data = fetch_leaderboard_data(LOGGED_IN_USER[0])

    # Create a Canvas for scrollable content
    canvas = tk.Canvas(main_frame, bg="white")
    canvas.pack(side="left", fill="both", expand=True)

    # Add a vertical scrollbar
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame to hold all tables
    table_container = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=table_container, anchor="nw")

    # Function to update scroll region
    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    table_container.bind("<Configure>", update_scroll_region)

    # Display all leaderboard tables (2 per row)
    courses = list(data.keys())
    for i in range(0, len(courses), 2):
        row_frame = tk.Frame(table_container, bg="white")
        row_frame.pack(fill="x", pady=10)

        # First table in the row
        if i < len(courses):
            course1 = courses[i]
            table_frame1 = tk.Frame(row_frame, bd=2, relief="groove")
            table_frame1.pack(side="left", fill="both", expand=True, padx=10)
            create_table(table_frame1, data[course1], course1)

        # Second table in the row
        if i + 1 < len(courses):
            course2 = courses[i + 1]
            table_frame2 = tk.Frame(row_frame, bd=2, relief="groove")
            table_frame2.pack(side="left", fill="both", expand=True, padx=10)
            create_table(table_frame2, data[course2], course2)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Leaderboard")
    root.geometry("800x600")

    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    create_leaderboard(main_frame)

    root.mainloop()