import tkinter as tk
from tkinter import ttk
import sqlite3

# Database connection
DATABASE_FILE = "quiz.db"

# Fetch questions for a course and category
def fetch_questions(course_id, category_id=None):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    if category_id:
        cursor.execute("""
            SELECT question, correct_ans
            FROM questions
            WHERE course_id = ? AND category_id = ?
        """, (course_id, category_id))
    else:
        cursor.execute("""
            SELECT question, correct_ans
            FROM questions
            WHERE course_id = ?
        """, (course_id,))
    questions = cursor.fetchall()
    conn.close()
    return questions

# Fetch categories for a course
def fetch_categories(course_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT category_id, category_name
        FROM categories
        WHERE course_id = ?
    """, (course_id,))
    categories = cursor.fetchall()
    conn.close()
    return categories

# Fetch courses from the database
def get_courses():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT course_id, coursename, coursedesc FROM courses")
    courses = cursor.fetchall()
    conn.close()
    return courses

# Display course description
def show_course_description(course_desc, frame_bottom2_inner, frame_bottom2_canvas):
    # Clear the existing content in the inner frame
    for widget in frame_bottom2_inner.winfo_children():
        widget.destroy()

    # Display the course description
    label = tk.Label(frame_bottom2_inner, text=course_desc, font=("Arial", 12), wraplength=500, justify="left")
    label.pack(pady=10, padx=10, fill="both", expand=True)

    # Update scroll region after content is added
    frame_bottom2_inner.update_idletasks()
    frame_bottom2_canvas.config(scrollregion=frame_bottom2_canvas.bbox("all"))

# Display questions for the selected category
def show_questions(course_id, category_name, frame_bottom2_inner, frame_bottom2_canvas):
    # Clear the existing content in the inner frame
    for widget in frame_bottom2_inner.winfo_children():
        widget.destroy()

    # Fetch questions based on the selected category
    if category_name == "All":
        questions = fetch_questions(course_id)
    else:
        categories = fetch_categories(course_id)
        category_id = next((cat[0] for cat in categories if cat[1] == category_name), None)
        questions = fetch_questions(course_id, category_id)

    # Display the questions
    for question, correct_ans in questions:
        question_frame = tk.Frame(frame_bottom2_inner, bd=2, relief="groove")
        question_frame.pack(fill="x", pady=5, padx=10)

        question_label = tk.Label(question_frame, text=f"Q: {question}", font=("Arial", 12), anchor="w")
        question_label.pack(fill="x", padx=5, pady=2)

        answer_label = tk.Label(question_frame, text=f"Correct Answer: {correct_ans}", font=("Arial", 12), anchor="w", fg="green")
        answer_label.pack(fill="x", padx=5, pady=2)

    # Update scroll region after content is added
    frame_bottom2_inner.update_idletasks()
    frame_bottom2_canvas.config(scrollregion=frame_bottom2_canvas.bbox("all"))


# Handle course button click
def on_course_button_click(course_id, course_desc, frame_bottom1, frame_bottom2_inner, frame_bottom2_canvas):
    # Clear the existing content in frame_bottom1
    for widget in frame_bottom1.winfo_children():
        widget.destroy()

    # Add a button to show course description
    desc_button = tk.Button(frame_bottom1, text="Show Course Description",
                            command=lambda: show_course_description(course_desc, frame_bottom2_inner, frame_bottom2_canvas))
    desc_button.pack(side="left", padx=10, pady=10)

    # Fetch categories for the course
    categories = fetch_categories(course_id)
    category_names = ["All"] + [cat[1] for cat in categories]

    # Add a dropdown for categories
    category_var = tk.StringVar(value="All")
    category_dropdown = ttk.Combobox(frame_bottom1, textvariable=category_var, values=category_names, state="readonly")
    category_dropdown.pack(side="left", padx=10, pady=10)

    # Add a button to show questions
    show_questions_button = tk.Button(frame_bottom1, text="Show Questions",
                                     command=lambda: show_questions(course_id, category_var.get(), frame_bottom2_inner, frame_bottom2_canvas))
    show_questions_button.pack(side="left", padx=10, pady=10)

# Main function to create the course page
def create_course_page(main_frame):
    # Fetch courses from the database
    courses = get_courses()

    # Upper Frame: Course Buttons with horizontal scrolling
    upper_frame_canvas = tk.Canvas(main_frame, bg="#f0f4f8", highlightthickness=0)
    upper_frame_canvas.pack(fill="x", pady=10, side="top")
    upper_frame = tk.Frame(upper_frame_canvas, bg="#f0f4f8")
    upper_frame_canvas.create_window((0, 0), window=upper_frame, anchor="nw")

    # Horizontal scrollbar for upper frame
    x_scrollbar = tk.Scrollbar(upper_frame_canvas, orient="horizontal", command=upper_frame_canvas.xview)
    upper_frame_canvas.configure(xscrollcommand=x_scrollbar.set, xscrollincrement='1')
    x_scrollbar.pack(side="top", fill="x",pady=50)
    upper_frame_canvas.configure(yscrollcommand=lambda *args: None) # Disable vertical scrolling for upper frame


    for course_id, course_name, course_desc in courses:
        course_button = tk.Button(upper_frame, text=course_name,
                                    command=lambda cid=course_id, desc=course_desc:
                                    on_course_button_click(cid, desc, frame_bottom1, frame_bottom2_inner, frame_bottom2_canvas))
        course_button.pack(side="left", padx=10, pady=10)

    upper_frame.update_idletasks()
    upper_frame_canvas.config(scrollregion=upper_frame_canvas.bbox("all"))
    upper_frame_canvas.config(width=main_frame.winfo_width()) # Adjust width if needed


    # Bottom Frame: Divided into two sub-frames
    bottom_frame = tk.Frame(main_frame, bg="#f0f4f8")
    bottom_frame.pack(fill="both", expand=True, side="top")

    # Frame Bottom 1: Course Description Button and Category Dropdown
    global frame_bottom1
    frame_bottom1 = tk.Frame(bottom_frame, bg="#f0f4f8")
    frame_bottom1.pack(fill="x", pady=10)

    # Frame Bottom 2: Display Course Description or Questions with vertical scrolling
    frame_bottom2_canvas = tk.Canvas(bottom_frame, bg="#f0f4f8", highlightthickness=0)
    frame_bottom2_canvas.pack(fill="both", expand=True)
    frame_bottom2_inner = tk.Frame(frame_bottom2_canvas, bg="#f0f4f8")
    frame_bottom2_canvas.create_window((0, 0), window=frame_bottom2_inner, anchor="nw")

    # Vertical scrollbar for bottom frame 2
    y_scrollbar = tk.Scrollbar(frame_bottom2_canvas, orient="vertical", command=frame_bottom2_canvas.yview)
    frame_bottom2_canvas.configure(yscrollcommand=y_scrollbar.set, yscrollincrement='1')
    y_scrollbar.pack(side="right", fill="y")
    frame_bottom2_canvas.configure(xscrollcommand=lambda *args: None) # Disable horizontal scrolling for bottom frame 2


    global frame_bottom2_inner_global
    frame_bottom2_inner_global = frame_bottom2_inner
    global frame_bottom2_canvas_global
    frame_bottom2_canvas_global = frame_bottom2_canvas

    # Show description of the first course by default
    if courses:
        first_course_id, first_course_name, first_course_desc = courses[0]
        on_course_button_click(first_course_id, first_course_desc, frame_bottom1, frame_bottom2_inner, frame_bottom2_canvas)
        show_course_description(first_course_desc, frame_bottom2_inner, frame_bottom2_canvas) # Directly show description


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Course Page")
    root.geometry("800x600")

    main_frame = tk.Frame(root, bg="#f0f4f8")
    main_frame.pack(fill="both", expand=True)

    create_course_page(main_frame)

    root.mainloop()