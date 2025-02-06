import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox


class QuizAdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App - Admin Dashboard")
        self.root.geometry("900x600")
        self.root.configure(bg="#E0E0E0")

        # Sidebar
        sidebar = tk.Frame(root, bg="#2C3E50")
        sidebar.place(relx=0, rely=0, relwidth=0.2, relheight=1)  # 20% width, full height

        profile_frame = tk.Frame(sidebar, bg="#2C3E50")
        profile_frame.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.2)  # Centered in sidebar

        profile_icon = tk.Label(profile_frame, text="🧑", font=("Arial", 40), bg="#2C3E50", fg="black")
        profile_icon.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        profile_name = tk.Label(profile_frame, text="Aayush Bohara", font=("Arial", 12, "bold"), bg="#2C3E50",
                                fg="white")
        profile_name.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        edit_profile_btn = tk.Button(profile_frame, text="Edit Profile", bg="#1F618D", fg="black", relief=tk.FLAT,
                                     width=15)
        edit_profile_btn.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        # Sidebar buttons
        buttons = ["Dashboard", "Users", "Courses", "LeaderBoard", "Mock Test", "Questions"]
        y_offset = 0.3  # Start below the profile frame
        for btn_text in buttons:
            btn = tk.Button(sidebar, text=btn_text, bg="#34495E", fg="black", relief=tk.FLAT)
            btn.place(relx=0.1, rely=y_offset, relwidth=0.8, relheight=0.07)
            y_offset += 0.09  # Increment for next button

        logout_btn = tk.Button(sidebar, text="🔓 LogOut", bg="#E74C3C", fg="black", relief=tk.FLAT)
        logout_btn.place(relx=0.1, rely=0.85, relwidth=0.8, relheight=0.07)

        # Main Dashboard
        main_frame = tk.Frame(root, bg="#E0E0E0")
        main_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)  # 80% width, full height

        header = tk.Label(main_frame, text="Dashboard", font=("Arial", 16, "bold"), bg="#E0E0E0")
        header.place(relx=0.05, rely=0.02)

        stats_frame = tk.Frame(main_frame, bg="#E0E0E0")
        stats_frame.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.1)

        stat_data = [("123", "Total Users")]

        for i, stat in enumerate(stat_data):
            stat_box = tk.Frame(stats_frame, bg="#34495E", width=120, height=60)
            stat_box.place(relx=i * 0.3, rely=0, relwidth=0.2, relheight=1)

            stat_label = tk.Label(stat_box, text=stat[0], font=("Arial", 14, "bold"), fg="white", bg="#34495E")
            stat_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            stat_desc = tk.Label(stat_box, text=stat[1], font=("Arial", 10), fg="white", bg="#34495E")
            stat_desc.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        # Add Button
        add_button = tk.Button(stats_frame, text="Add User", bg="#1F618D", fg="black", relief=tk.FLAT, command=self.register_user)
        add_button.place(relx=0.8, rely=0.2, relwidth=0.15, relheight=0.6)

        # No. of user displayed
        def user_no_selected(selected_user_no):
            # Clear the existing rows in the Treeview
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insert only the selected number of rows
            num_rows = int(selected_user_no)
            for i in range(min(num_rows, len(self.rows))):  # Ensure we don't exceed the total number of rows
                self.tree.insert("", "end", values=self.rows[i])

            # Adjust the height of the Treeview to match the number of rows
            self.tree.configure(height=num_rows)

        no_of_user = ["3", "6", "9", "12"]
        selected_user_no = StringVar(value="No. of user displayed")

        selected_user_no = OptionMenu(main_frame, selected_user_no, *no_of_user, command=user_no_selected)
        selected_user_no.config(font=("Arial", 10), width=13)
        selected_user_no.place(relx=0.05, rely=0.25)

        # Filter with
        def filter_info(filter_with):
            # Clear the existing rows in the Treeview
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Sort rows based on the selected filter criteria
            if filter_with == "Username":
                # Sort by username (alphabetically)
                sorted_rows = sorted(self.rows, key=lambda x: x[1].lower())  # Case-insensitive sorting
            elif filter_with == "SN":
                # Sort by serial number (ascending order)
                sorted_rows = sorted(self.rows, key=lambda x: int(x[0]))
            else:
                # Default: No sorting
                sorted_rows = self.rows

            # Insert sorted rows into the Treeview
            for row in sorted_rows:
                self.tree.insert("", "end", values=row)

            # Adjust the height of the Treeview to match the number of rows
            self.tree.configure(height=len(sorted_rows))

        filter_value = ["Username", "SN"]  # Updated filter options
        filter_with = StringVar(value="Filter With:")

        filter_with = OptionMenu(main_frame, filter_with, *filter_value, command=filter_info)
        filter_with.config(font=("Arial", 10), width=13)
        filter_with.place(relx=0.25, rely=0.25)

        # Search Bar
        search_label = tk.Label(main_frame, text="Search:", font=("Arial", 13), bg="#E0E0E0",fg='black')
        search_label.place(relx=0.45, rely=0.25)

        self.search_entry = tk.Entry(main_frame, font=("Arial", 10), width=20)
        self.search_entry.place(relx=0.52, rely=0.25)

        search_button = tk.Button(main_frame, text="Search", bg="#1F618D", fg="black", relief=tk.FLAT,
                                  command=self.search_table)
        search_button.place(relx=0.72, rely=0.25, width=80)

        # Table Data
        table_frame = tk.Frame(main_frame, bg="#E0E0E0")
        table_frame.place(relx=0.05, rely=0.35, relwidth=0.9, relheight=0.5)

        columns = ("Sn", "Username", "Name", "Contact", "Email")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=150)

        # Insert rows
        self.rows = [
            ("1", "poplol2", "Ram Rai", "9876543210", "a@gmail.com"),
            ("2", "user123", "John Doe", "1234567890", "john@example.com"),
            ("3", "testuser", "Jane Doe", "0987654321", "jane@example.com"),
            ("4", "demo", "Demo User", "1122334455", "demo@example.com"),
            ("5", "user5", "User Five", "1111111111", "user5@example.com"),
            ("6", "user6", "User Six", "2222222222", "user6@example.com"),
            ("7", "user7", "User Seven", "3333333333", "user7@example.com"),
            ("8", "user8", "User Eight", "4444444444", "user8@example.com"),
            ("9", "user9", "User Nine", "5555555555", "user9@example.com"),
            ("10", "user10", "User Ten", "6666666666", "user10@example.com"),
        ]

        # Initially display all rows
        for row in self.rows:
            self.tree.insert("", "end", values=row)

        # Set the height of the Treeview to match the number of rows initially
        self.tree.configure(height=len(self.rows))

        self.tree.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Edit and Delete Buttons
        edit_button = tk.Button(main_frame, text="Edit", bg="#1F618D", fg="black", relief=tk.FLAT, command=self.edit_user)
        edit_button.place(relx=0.05, rely=0.9, relwidth=0.1, relheight=0.05)

        delete_button = tk.Button(main_frame, text="Delete", bg="#E74C3C", fg="black", relief=tk.FLAT, command=self.delete_user)
        delete_button.place(relx=0.15, rely=0.9, relwidth=0.1, relheight=0.05)

    def search_table(self):
        # Get the search term from the entry widget
        search_term = self.search_entry.get().strip().lower()

        # Clear the existing rows in the Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Filter rows based on the search term
        filtered_rows = []
        for row in self.rows:
            if any(search_term in str(cell).lower() for cell in row):  # Search across all columns
                filtered_rows.append(row)

        # Insert filtered rows into the Treeview
        for row in filtered_rows:
            self.tree.insert("", "end", values=row)

        # Adjust the height of the Treeview to match the number of filtered rows
        self.tree.configure(height=len(filtered_rows))

    def register_user(self):
        # Open a new window for user registration
        register_window = tk.Toplevel(self.root)
        register_window.title("Register User")
        register_window.geometry("400x300")

        # Add labels and entry fields for user registration
        tk.Label(register_window, text="Username:").place(relx=0.1, rely=0.1)
        username_entry = tk.Entry(register_window)
        username_entry.place(relx=0.3, rely=0.1)

        tk.Label(register_window, text="Name:").place(relx=0.1, rely=0.2)
        name_entry = tk.Entry(register_window)
        name_entry.place(relx=0.3, rely=0.2)

        tk.Label(register_window, text="Contact:").place(relx=0.1, rely=0.3)
        contact_entry = tk.Entry(register_window)
        contact_entry.place(relx=0.3, rely=0.3)

        tk.Label(register_window, text="Email:").place(relx=0.1, rely=0.4)
        email_entry = tk.Entry(register_window)
        email_entry.place(relx=0.3, rely=0.4)

        # Add a button to submit the registration
        submit_button = tk.Button(register_window, text="Submit", command=lambda: self.submit_registration(
            username_entry.get(), name_entry.get(), contact_entry.get(), email_entry.get(), register_window))
        submit_button.place(relx=0.4, rely=0.6)

    def submit_registration(self, username, name, contact, email, window):
        # Add the new user to the rows list
        new_user = (str(len(self.rows) + 1), username, name, contact, email)
        self.rows.append(new_user)

        # Insert the new user into the Treeview
        self.tree.insert("", "end", values=new_user)

        # Close the registration window
        window.destroy()

    def edit_user(self):
        # Get the selected user from the Treeview
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a user to edit.")
            return

        # Get the selected user's details
        selected_user = self.tree.item(selected_item, "values")

        # Open a new window for editing the user
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit User")
        edit_window.geometry("400x300")

        # Add labels and entry fields for editing the user
        tk.Label(edit_window, text="Username:").place(relx=0.1, rely=0.1)
        username_entry = tk.Entry(edit_window)
        username_entry.insert(0, selected_user[1])
        username_entry.place(relx=0.3, rely=0.1)

        tk.Label(edit_window, text="Name:").place(relx=0.1, rely=0.2)
        name_entry = tk.Entry(edit_window)
        name_entry.insert(0, selected_user[2])
        name_entry.place(relx=0.3, rely=0.2)

        tk.Label(edit_window, text="Contact:").place(relx=0.1, rely=0.3)
        contact_entry = tk.Entry(edit_window)
        contact_entry.insert(0, selected_user[3])
        contact_entry.place(relx=0.3, rely=0.3)

        tk.Label(edit_window, text="Email:").place(relx=0.1, rely=0.4)
        email_entry = tk.Entry(edit_window)
        email_entry.insert(0, selected_user[4])
        email_entry.place(relx=0.3, rely=0.4)

        # Add a button to submit the changes
        submit_button = tk.Button(edit_window, text="Submit", command=lambda: self.submit_edit(
            selected_item, username_entry.get(), name_entry.get(), contact_entry.get(), email_entry.get(), edit_window))
        submit_button.place(relx=0.4, rely=0.6)

    def submit_edit(self, selected_item, username, name, contact, email, window):
        # Update the user's details in the rows list
        for i, row in enumerate(self.rows):
            if row[0] == self.tree.item(selected_item, "values")[0]:
                self.rows[i] = (row[0], username, name, contact, email)
                break

        # Update the Treeview with the new details
        self.tree.item(selected_item, values=(self.rows[i]))

        # Close the edit window
        window.destroy()

    def delete_user(self):
        # Get the selected user from the Treeview
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a user to delete.")
            return

        # Display a confirmation popup
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?")
        if confirm:
            # Remove the user from the rows list
            selected_user = self.tree.item(selected_item, "values")
            self.rows = [row for row in self.rows if row[0] != selected_user[0]]

            # Remove the user from the Treeview
            self.tree.delete(selected_item)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizAdminDashboard(root)
    root.mainloop()