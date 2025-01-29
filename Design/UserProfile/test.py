from tkinter import *

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

# Labels and Entries
labels_entries = [
    ("Name", 70, 320, user[0]),
    ("User Name", 70, 400, user[1]),
    ("Contact Number", 70, 480, user[2]),
    ("Email", 70, 560, user[3]),
    ("New Password", 640, 320, ""),
    ("Confirm Password", 640, 400, "")
]

for text, x, y, value in labels_entries:
    Label(root, text=text).place(x=x, y=y)
    entry = Entry(root, width=35)
    entry.place(x=x, y=y+20)
    entry.insert(0, value)

# Buttons
Button(text='UPDATE', font=('Arial', 14, 'bold')).place(x=83, y=690)
Button(text='CANCEL', font=('Arial', 14, 'bold')).place(x=800, y=690)

root.mainloop()