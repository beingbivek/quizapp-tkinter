import tkinter as tk
from tkinter import ttk

def create_page(container, text):
    """Creates a page with a label displaying the given text."""
    frame = ttk.Frame(container, style="TFrame")
    label = ttk.Label(frame, text=text, font=("Arial", 16), anchor="center", background="#f0f4f8", foreground="#003366")
    label.pack(expand=True, fill="both", padx=10, pady=10)
    return frame

def main():
    root = tk.Tk()
    root.title("Courses and Topics")
    root.geometry("800x600")

    # Set styles
    style = ttk.Style()
    style.theme_use("default")
    style.configure("TNotebook", background="#003366", borderwidth=0)
    style.configure("TNotebook.Tab", background="#00509e", foreground="white", font=("Arial", 12, "bold"), padding=(10, 5))
    style.map("TNotebook.Tab", background=[("selected", "#003366")], foreground=[("selected", "white")])
    style.configure("TFrame", background="#f0f4f8")

    # Outer Notebook for Courses
    course_tabs = ttk.Notebook(root)
    course_tabs.pack(expand=True, fill="both")

    # Sample Courses
    courses = {
        "CEE": ["Exam Pattern", "Questions", "Mock Test"],
        "IOE": ["Exam Pattern", "Questions", "Mock Test"],
        "Driving License Exam": ["Exam Pattern", "Questions", "Mock Test"],
         'Loksewa Exam' : ['Exam Pattern', 'Questions', 'Mock Test']
}
    

    for course_name, topics in courses.items():
        # Create a tab for each course
        course_tab = ttk.Frame(course_tabs, style="TFrame")
        course_tabs.add(course_tab, text=course_name)

        # Inner Notebook for Topics
        topic_tabs = ttk.Notebook(course_tab)
        topic_tabs.pack(expand=True, fill="both")

        for topic_name in topics:
            # Create a tab for each topic under the course
            topic_tab = create_page(topic_tabs, f"Content for {topic_name}")
            topic_tabs.add(topic_tab, text=topic_name)

    root.mainloop()

if __name__ == "__main__":
    main()
