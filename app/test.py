import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Treeview with Ellipsis")
root.geometry("500x300")

# Create a custom style for Treeview with ellipsis
style = ttk.Style()

# Define a custom layout for Treeview cells
style.layout("Custom.Treeview.Cell", [
    ("Treeitem.padding", {
        "sticky": "nswe",
        "children": [
            ("Treeitem.text", {
                "sticky": "w",
                "ellipsis": "...",  # Add ellipsis for truncated text
            })
        ]
    })
])

# Apply the custom style to the Treeview
style.configure("Custom.Treeview", 
                font=("Arial", 12), 
                rowheight=25, 
                fieldbackground="#f0f0f0")
style.configure("Custom.Treeview.Heading", 
                font=("Arial", 12, "bold"))
style.map("Custom.Treeview", 
          background=[("selected", "#0078d7")], 
          foreground=[("selected", "white")])

# Create a Treeview widget with the custom style
tree = ttk.Treeview(root, columns=("Name", "Description"), show="headings", style="Custom.Treeview")
tree.heading("Name", text="Name")
tree.heading("Description", text="Description")
tree.pack(fill="both", expand=True)

# Set column widths
tree.column("Name", width=100, anchor="w")
tree.column("Description", width=200, anchor="w")

# Insert sample data
data = [
    ("John Doe", "This is a very long description that will be truncated with an ellipsis."),
    ("Jane Smith", "Another long description that won't fit in the cell."),
    ("Alice Johnson", "Short text"),
    ("Bob Brown", "This is another example of a long description that will be truncated.")
]

for item in data:
    tree.insert("", "end", values=item)

# Run the application
root.mainloop()