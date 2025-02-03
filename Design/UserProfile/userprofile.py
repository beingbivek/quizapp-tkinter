from tkinter import *

def update_info():
    # Get the updated values from the entry fields
    updated_user = [
        entries[0].get(),
        entries[1].get(),
        entries[2].get(),
        entries[3].get(),
        entries[4].get(),
        entries[5].get()
    ]
    
    # Update the user list with the new values
    user[0] = updated_user[0]  # Update Name
    user[1] = updated_user[1]  # Update User Name
    user[2] = updated_user[2]  # Update Contact Number
    user[3] = updated_user[3]  # Update Email
    
    # Clear and re-insert the updated values into the entry fields
    for i, entry in enumerate(entries):
        entry.delete(0, END)  # Clear the current value
        entry.insert(0, updated_user[i])  # Insert the updated value
    
    print("Updated User Info:", updated_user)  # Print to console for debugging

def cancel():
    root.destroy()  # Close the application

root = Tk()
root.title("User Profile")
root.geometry("1000x800")

user = ['Mukesh Babu Acharya', 'Babu.net', '9862148844', 'babu@gmail.com']

# Frames
mainframe = Frame(root, bd=2, relief="ridge")
mainframe.place(x=0, y=0, width=1000, height=800)

secframe = Frame(root, bd=2, relief='ridge')
secframe.place(x=50, y=50, width=900, height=700)

# Canvas for the circle
canvas = Canvas(root, width=250, height=250)
canvas.place(x=350, y=70)
canvas.create_oval(80, 80, 200, 200, fill="lightgrey", outline="black")

# Username below canvas
Label(text=user[1]).place(x=460,y=270)

# Labels and Entries
labels_entries = [
    ("Name", 70, 320, user[0]),
    ("User Name", 70, 400, user[1]),
    ("Contact Number", 70, 480, user[2]),
    ("Email", 70, 560, user[3]),
    ("New Password", 640, 320, ""),
    ("Confirm Password", 640, 400, "")
]

entries = []  # List to store entry widgets

for text, x, y, value in labels_entries:
    Label(root, text=text).place(x=x, y=y)
    entry = Entry(root, width=35)
    entry.place(x=x, y=y+20)
    entry.insert(0, value)
    entries.append(entry)  # Add the entry widget to the list

# Buttons
Button(root, text='UPDATE', font=('Arial', 14, 'bold'), command=update_info).place(x=83, y=690)
Button(root, text='CANCEL', font=('Arial', 14, 'bold'), command=cancel).place(x=800, y=690)

root.mainloop()