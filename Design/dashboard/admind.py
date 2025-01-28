import tkinter as tk
from tkinter import ttk

class QuizAdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App - Admin Dashboard")
        self.root.geometry("900x600")
        self.root.configure(bg="#E0E0E0")

        # Sidebar
        sidebar = tk.Frame(root, bg="#2C3E50", width=200, height=600)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        profile_frame = tk.Frame(sidebar, bg="#2C3E50")
        profile_frame.pack(pady=20)
        
        profile_icon = tk.Label(profile_frame, text="🧑", font=("Arial", 40), bg="#2C3E50", fg="white")
        profile_icon.pack()
        
        profile_name = tk.Label(profile_frame, text="Aayush Bohara", font=("Arial", 12, "bold"), bg="#2C3E50", fg="white")
        profile_name.pack()
        
        edit_profile_btn = tk.Button(profile_frame, text="Edit Profile", bg="#1F618D", fg="white", relief=tk.FLAT, width=15)
        edit_profile_btn.pack(pady=5)

        # Sidebar buttons
        buttons = ["Dashboard", "Users", "Courses", "LeaderBoard", "Mock Test", "Questions"]
        for btn_text in buttons:
            btn = tk.Button(sidebar, text=btn_text, bg="#34495E", fg="white", relief=tk.FLAT, width=20, height=2)
            btn.pack(pady=2)
        
        logout_btn = tk.Button(sidebar, text="🔓 LogOut", bg="#E74C3C", fg="white", relief=tk.FLAT, width=20, height=2)
        logout_btn.pack(pady=20)
        
        # Main Dashboard
        main_frame = tk.Frame(root, bg="#E0E0E0")
        main_frame.pack(expand=True, fill=tk.BOTH)

        header = tk.Label(main_frame, text="Dashboard", font=("Arial", 16, "bold"), bg="#E0E0E0")
        header.pack(pady=10)
        
        stats_frame = tk.Frame(main_frame, bg="#E0E0E0")
        stats_frame.pack()
        
        stat_data = [("123", "Total Users"), ("4", "Total Courses"), ("123", "Total Subcategories"), ("123", "Total Questions")]
        
        for stat in stat_data:
            stat_box = tk.Frame(stats_frame, bg="#34495E", width=120, height=60)
            stat_box.pack_propagate(False)
            stat_box.pack(side=tk.LEFT, padx=10, pady=10)
            
            stat_label = tk.Label(stat_box, text=stat[0], font=("Arial", 14, "bold"), fg="white", bg="#34495E")
            stat_label.pack()
            stat_desc = tk.Label(stat_box, text=stat[1], font=("Arial", 10), fg="white", bg="#34495E")
            stat_desc.pack()

        # Table Data
        table_frame = tk.Frame(main_frame)
        table_frame.pack(pady=20)

        columns = ("Particulars", "Numbers", "Remark")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=150)
        
        tree.insert("", "end", values=("User Registered Today", "56", "Grown by 10%"))
        tree.insert("", "end", values=("Mock Test Today", "50", "Grown by 10%"))
        
        tree.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizAdminDashboard(root)
    root.mainloop()
