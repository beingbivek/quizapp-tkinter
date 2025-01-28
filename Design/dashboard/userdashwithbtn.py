import tkinter as tk
from tkinter import ttk

class QuizAppUserDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz App - User Dashboard")
        self.geometry("800x600")

        # Sidebar
        sidebar = tk.Frame(self, width=200, bg="#2C3E50")
        sidebar.pack(expand=False, fill="y", side="left", anchor="nw")
        
        profile_label = tk.Label(sidebar, text="Aayush Bohara", bg="#2C3E50", fg="white", font=("Arial", 12, "bold"))
        profile_label.pack(pady=10)
        
        edit_button = tk.Button(sidebar, text="Edit Profile", bg="#1A252F", fg="white")
        edit_button.pack(pady=5)
        
        buttons = ["Dashboard", "Courses", "LeaderBoard", "Mock Test", "About US"]
        for btn in buttons:
            button = tk.Button(sidebar, text=btn, bg="#34495E", fg="white")
            button.pack(fill="x")
        
        logout_button = tk.Button(sidebar, text="LogOut", bg="#E74C3C", fg="white")
        logout_button.pack(fill="x", pady=20)
        
        # Main Content
        main_content = tk.Frame(self, bg="white")
        main_content.pack(expand=True, fill="both", side="right")
        
        question_label = tk.Label(main_content, text="Question of the day!", font=("Arial", 16, "bold"), bg="white")
        question_label.pack(pady=10)
        
        question_text = tk.Label(main_content, text="Topic: Loksewa/Animal\nQ. How fast can a Cheetah run?", font=("Arial", 12), bg="white")
        question_text.pack()
        
        # Question Options
        self.answer_var = tk.StringVar()
        options = ["80 kmph", "90 kmph", "100 kmph", "120 kmph"]
        for option in options:
            rb = tk.Radiobutton(main_content, text=option, variable=self.answer_var, value=option, bg="white")
            rb.pack(anchor="w")
        
        submit_button = tk.Button(main_content, text="Submit Answer", bg="#2C3E50", fg="white", command=self.submit_answer)
        submit_button.pack(pady=10)
        
        # Progress Table
        progress_label = tk.Label(main_content, text="Your Progress", font=("Arial", 14, "bold"), bg="white")
        progress_label.pack(pady=10)
        
        columns = ("SN", "Courses", "Tackled", "Correct", "Incorrect")
        progress_table = ttk.Treeview(main_content, columns=columns, show='headings')
        
        for col in columns:
            progress_table.heading(col, text=col)
        
        progress_table.insert('', 'end', values=(1, "CEE", 40, 30, 10))
        progress_table.insert('', 'end', values=(2, "IOE", 38, 8, 30))
        progress_table.insert('', 'end', values=(3, "Driving", 41, 1, 40))
        progress_table.insert('', 'end', values=(4, "LokSewa", 45, 40, 5))
        
        progress_table.pack()
        
        # Mock Test Results
        test_label = tk.Label(main_content, text="Previous Mock Test Results", font=("Arial", 14, "bold"), bg="white")
        test_label.pack(pady=10)
        
        test_columns = ("SN", "Mock TestID", "Datetime", "Course", "Result")
        test_table = ttk.Treeview(main_content, columns=test_columns, show='headings')
        
        for col in test_columns:
            test_table.heading(col, text=col)
        
        test_table.insert('', 'end', values=(1, "CEE12", "2024/5/20 15:20", "CEE", "50/100"))
        test_table.insert('', 'end', values=(2, "IOE312", "2024/5/20 15:20", "IOE", "50/100"))
        test_table.insert('', 'end', values=(3, "Driving123", "2024/5/20 15:20", "Driving", "50/100"))
        test_table.insert('', 'end', values=(4, "LokSewa4334", "2024/5/20 15:20", "Loksewa", "50/100"))
        
        test_table.pack()
    
    def submit_answer(self):
        selected_answer = self.answer_var.get()
        print(f"Submitted Answer: {selected_answer}")

if __name__ == "__main__":
    app = QuizAppUserDashboard()
    app.mainloop()
