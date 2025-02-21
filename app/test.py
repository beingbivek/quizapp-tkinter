# import tkinter as tk
# from tkinter import ttk

# def on_treeview_select(event):
#     selected_item = category_table.focus()
#     item_data = category_table.item(selected_item)
#     print("Selected item data:", item_data)

# root = tk.Tk()
# category_table_frame = tk.Frame(root)
# category_table_frame.pack()

# columns = ('category_id', 'categoryname', 'coursename', 'actions')
# category_table = ttk.Treeview(category_table_frame, columns=columns, show='headings')

# category_table.heading('category_id', text='Category ID', anchor='center')
# category_table.heading('categoryname', text='Category Name', anchor='center')
# category_table.heading('coursename', text='Course Name', anchor='center')
# category_table.heading('actions', text='Actions', anchor='center')

# category_table.column('category_id', anchor='center')
# category_table.column('categoryname', anchor='center')
# category_table.column('coursename', anchor='center')
# category_table.column('actions', anchor='center')

# category_table.pack()

# # Insert sample data
# category_table.insert('', 'end', values=(1, 'Category 1', 'Course 1', 'Edit/Delete'))
# category_table.insert('', 'end', values=(2, 'Category 2', 'Course 2', 'Edit/Delete'))

# # Bind the selection event to the on_treeview_select function
# category_table.bind('<<TreeviewSelect>>', on_treeview_select)

# root.mainloop()

import tkinter as tk
from tkinter import ttk

def on_treeview_select(event):
    selected_item = category_table.focus()
    item_data = category_table.item(selected_item)
    print("Selected item data:", item_data)

def on_edit():
    selected_item = category_table.focus()
    item_data = category_table.item(selected_item)
    if selected_item:
        print("Edit item:", item_data)
        # Implement your edit functionality here

def on_delete():
    selected_item = category_table.focus()
    if selected_item:
        category_table.delete(selected_item)
        print("Deleted item:", selected_item)
        # Implement your delete functionality here

root = tk.Tk()
category_table_frame = tk.Frame(root)
category_table_frame.pack()

columns = ('category_id', 'categoryname', 'coursename', 'actions')
category_table = ttk.Treeview(category_table_frame, columns=columns, show='headings')

category_table.heading('category_id', text='Category ID', anchor='center')
category_table.heading('categoryname', text='Category Name', anchor='center')
category_table.heading('coursename', text='Course Name', anchor='center')
category_table.heading('actions', text='Actions', anchor='center')

category_table.column('category_id', anchor='center')
category_table.column('categoryname', anchor='center')
category_table.column('coursename', anchor='center')
category_table.column('actions', anchor='center')

category_table.pack()

# Insert sample data
category_table.insert('', 'end', values=(1, 'Category 1', 'Course 1', 'Edit/Delete'))
category_table.insert('', 'end', values=(2, 'Category 2', 'Course 2', 'Edit/Delete'))

# Bind the selection event to the on_treeview_select function
category_table.bind('<<TreeviewSelect>>', on_treeview_select)

# Create Edit and Delete buttons
edit_button = tk.Button(root, text="Edit", command=on_edit)
edit_button.pack(side=tk.LEFT, padx=10, pady=10)

delete_button = tk.Button(root, text="Delete", command=on_delete)
delete_button.pack(side=tk.LEFT, padx=10, pady=10)

root.mainloop()
