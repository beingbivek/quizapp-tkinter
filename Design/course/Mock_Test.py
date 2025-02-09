import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog

# Function to add a new mock test
def add_mock_test():
    mock_test_name = f"MockTest{len(mock_tests) + 1}"
    mock_tests.append(mock_test_name)
    update_mock_test_table()

# Function to edit an existing mock test
def edit_mock_test(index):
    new_name = simpledialog.askstring("Edit Mock Test", "Enter new mock test name:", initialvalue=mock_tests[index])
    if new_name:
        mock_tests[index] = new_name
        update_mock_test_table()

# Function to delete a mock test
def delete_mock_test(index):
    del mock_tests[index]
    update_mock_test_table()

# Function to update the mock test table
def update_mock_test_table():
    for row in mock_test_table.get_children():
        mock_test_table.delete(row)
    for i, test in enumerate(mock_tests):
        mock_test_table.insert("", "end", values=(i+1, test, "Edit", "Delete"))

# Event handler for clicking on the mock test table
def on_mock_test_click(event):
    selected_item = mock_test_table.selection()
    if not selected_item:
        return
    item = selected_item[0]
    values = mock_test_table.item(item, "values")
    
    if len(values) < 4:
        return
    
    index = int(values[0]) - 1  # Get index of the mock test
    
    col_id = mock_test_table.identify_column(event.x)
    
    if col_id == "#3":  # Edit column
        edit_mock_test(index)
    elif col_id == "#4":  # Delete column
        delete_mock_test(index)

# Function to open the Add Question UI
def open_add_question_ui():
    add_question_window = tk.Toplevel(root)
    add_question_window.title("Add Questions To Mock Test")
    add_question_window.geometry("500x400")
    
    tk.Label(add_question_window, text="Mock Test Name:").pack()
    ttk.Combobox(add_question_window, values=mock_tests).pack()
    
    tk.Label(add_question_window, text="Courses:").pack()
    courses_combo = ttk.Combobox(add_question_window, values=["IOE", "CEE", "Driving Exam", "Loksewa"])
    courses_combo.pack()
    
    tk.Label(add_question_window, text="Categories:").pack()
    categories_combo = ttk.Combobox(add_question_window, values=["Physics", "Botany"])
    categories_combo.pack()
    
    tk.Label(add_question_window, text="No of Questions:").pack()
    questions_entry = tk.Entry(add_question_window)
    questions_entry.pack()
    
    # Function to save a question to the table
    def save_question():
        course = courses_combo.get()
        category = categories_combo.get()
        num_questions = questions_entry.get()
        if not (course and category and num_questions.isdigit()):
            messagebox.showerror("Error", "Please fill all fields correctly.")
            return
        questions_data.append((course, category, num_questions))
        update_questions_table()
    
    # Function to edit a question
    def edit_question(index):
        new_course = simpledialog.askstring("Edit Question", "Enter new course:", initialvalue=questions_data[index][0])
        new_category = simpledialog.askstring("Edit Question", "Enter new category:", initialvalue=questions_data[index][1])
        new_num_questions = simpledialog.askstring("Edit Question", "Enter new number of questions:", initialvalue=questions_data[index][2])
        if new_course and new_category and new_num_questions.isdigit():
            questions_data[index] = (new_course, new_category, new_num_questions)
            update_questions_table()
    
    # Function to delete a question
    def delete_question(index):
        del questions_data[index]
        update_questions_table()
    
    # Function to update the questions table
    def update_questions_table():
        for row in questions_table.get_children():
            questions_table.delete(row)
        for i, (course, category, num_questions) in enumerate(questions_data):
            questions_table.insert("", "end", values=(i+1, course, category, num_questions, "Edit", "Delete"))
    
    # Event handler for clicking on the questions table
    def on_question_click(event):
        selected_item = questions_table.selection()
        if not selected_item:
            return
        item = selected_item[0]
        values = questions_table.item(item, "values")
        
        if len(values) < 6:
            return
        
        index = int(values[0]) - 1
        col_id = questions_table.identify_column(event.x)
        
        if col_id == "#5":  # Edit column
            edit_question(index)
        elif col_id == "#6":  # Delete column
            delete_question(index)
    
    tk.Button(add_question_window, text="Save", command=save_question).pack()
    
    # Creating the questions table
    questions_table = ttk.Treeview(add_question_window, columns=("S.N", "Course", "Category", "Questions", "Edit", "Delete"), show="headings")
    for col in ["S.N", "Course", "Category", "Questions", "Edit", "Delete"]:
        questions_table.heading(col, text=col)
    questions_table.bind("<ButtonRelease-1>", on_question_click)
    questions_table.pack()

# Initialize data lists
mock_tests = []
questions_data = []  # Add this line to define the list before using it

# Create main application window
root = tk.Tk()
root.title("Mock Test Management")
root.geometry("600x500")

mock_tests = []

# Button to add a mock test
tk.Button(root, text="Add Mock Test", command=add_mock_test).pack()

# Creating the mock test table
mock_test_table = ttk.Treeview(root, columns=("S.N", "Mock Test Name", "Edit", "Delete"), show="headings")

for col in ["S.N", "Mock Test Name", "Edit", "Delete"]:
    mock_test_table.heading(col, text=col)

mock_test_table.bind("<ButtonRelease-1>", on_mock_test_click)
mock_test_table.pack()

# Button to open the Add Question UI
tk.Button(root, text="Add Questions to Test", command=open_add_question_ui).pack()

root.mainloop()
