from tkinter import *

def update_info():
    
    update_window = Toplevel(root)
    update_window.title("Update User Info")
    update_window.geometry("500x350")

    
    update_labels_entries = [
        ("Name", 20, 20, user[0]),
        ("User Name", 20, 70, user[1]),
        ("Contact Number", 20, 120, user[2]),
        ("Email", 20, 170, user[3]),
        ("New Password", 20, 220, ""),
        ("Confirm Password", 20, 270, "")
    ]

    update_entries = []  

    for text, x, y, value in update_labels_entries:
        Label(update_window, text=text).place(x=x, y=y)
        
        if "new password" in text.lower() or "confirm password" in text.lower():
            entry = Entry(update_window, width=25,show='*')
        else:
            entry = Entry(update_window, width=25,)
            
        entry.place(x=x + 120, y=y)
        entry.insert(0, value)
        update_entries.append(entry)  

    def save_updates():
        
        updated_user = [
            update_entries[0].get(),
            update_entries[1].get(),
            update_entries[2].get(),
            update_entries[3].get(),
            update_entries[4].get(),
            update_entries[5].get()
        ]

        user[0] = updated_user[0]  
        user[1] = updated_user[1]  
        user[2] = updated_user[2]  
        user[3] = updated_user[3]  
        f = open(r'C:\Project\quizapp-tkinter\Design\UserProfile\userprofile.txt','w')
        for i in user:
            if user.index(i) == 0:
                f.write(i+'\n')
            else:
                f.write(i)
        f.close()

        
        for i, entry in enumerate(entries):
            entry.delete(0, END)  
            entry.insert(0, updated_user[i])  

        print("Updated User Info:", updated_user)  
        update_window.destroy() 

    Button(update_window, text='SAVE', font=('Arial', 12, 'bold'), command=save_updates).place(x=400, y=300)

def cancel():
    root.destroy()  

root = Tk()
root.title("User Profile")
root.geometry("1000x800")

f = open(r'C:\Project\quizapp-tkinter\Design\UserProfile\userprofile.txt')
user = f.readlines()
f.close()

mainframe = Frame(root, bd=2, relief="ridge")
mainframe.place(x=0, y=0, width=1000, height=800)

secframe = Frame(root, bd=2, relief='ridge')
secframe.place(x=50, y=50, width=900, height=700)


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

entries = []  

for text, x, y, value in labels_entries:
    Label(root, text=text).place(x=x, y=y)
    entry = Entry(root, width=35)
    entry.place(x=x, y=y+20)
    entry.insert(0, value)
    entries.append(entry)  

# Buttons
Button(root, text='UPDATE', font=('Arial', 14, 'bold'), command=update_info).place(x=83, y=690)
Button(root, text='CANCEL', font=('Arial', 14, 'bold'), command=cancel).place(x=800, y=690)

root.mainloop()