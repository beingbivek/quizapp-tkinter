secframe = Frame(root, bd=2, relief='ridge')
secframe.place(x=50, y=50, width=900, height=700)

username = Label(root, text=users[3], font=('Arial', 14, 'bold')).place(x=462, y=255)

canvas = Canvas(root, width=200, height=200)
canvas.place(x=420, y=55)
canvas.create_oval(50, 50, 150, 150)


# Labels and Entries
labels_entries = [
    ("Name", 70, 320, users[1]),
    ("User Name", 70, 400, users[3]),
    ("Contact Number", 70, 480, users[4]),
    ("Email", 70, 560, users[2]),
    ("Address", 640, 480, users[5]),
    ("New Password", 640, 320, "",),
    ("Confirm Password", 640, 400, "")
]


entries = []
for text, x, y, value in labels_entries:
    Label(root, text=text).place(x=x, y=y)
    if text in ["New Password", "Confirm Password"]:
        entry = Entry(root, width=35, show="*")  # Mask the password fields
    else:
        entry = Entry(root, width=35)
    entry.place(x=x, y=y+20)
    entry.insert(0, value)
    entries.append(entry)

# Buttons
Button(text='UPDATE', bg="#34495E", fg="black", font=('Arial', 14, 'bold'), command=update_profile).place(x=83, y=690)