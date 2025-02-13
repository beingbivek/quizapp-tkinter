from tkinter import *
import sqlite3
import pybase64


# Add user in db
def submit():
    # password changed to base64 encrypt
    secret = password.get()
    secret = secret.encode('ascii')
    secret = pybase64.b64encode(secret)
    secret = secret.decode('ascii')
    
    # To decrypt/decode password to original password
    '''
    secret = password.get() # put the password variable
    secret = secret.encode('ascii')
    secret = pybase64.b64decode(secret)
    secret = secret.decode('ascii') # this is the final password
    '''

    # connect to db
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('''
    INSERT INTO users (fullname, email, username, contact, address, password)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (full_name.get(), email.get(), user_name.get(), contact.get(), address.get(), secret)
    )
    full_name.delete(0,END)
    email.delete(0,END)
    user_name.delete(0,END)
    contact.delete(0,END)
    address.delete(0,END)
    password.delete(0,END)
    conn.commit()
    conn.close()

root = Tk()
root.geometry('400x400')
root.title('Admin Dashboard')

full_name = Entry(root, width=80)
full_name.grid(row = 0 , column= 0,padx=20)
email = Entry(root, width=80)
email.grid(row = 1 , column= 0,padx=20)
user_name = Entry(root, width=80)
user_name.grid(row = 2 , column= 0,padx=20)
contact = Entry(root, width=80)
contact.grid(row = 3 , column= 0,padx=20)
address = Entry(root, width=80)
address.grid(row = 4 , column= 0,padx=20)
password = Entry(root, width=80,show='*')
password.grid(row = 5 , column= 0,padx=20)

# Create submit btn
submit_btn = Button(root, text='Add User', command=submit)
submit_btn.grid(row=6,column=0,columnspan=2, padx=10,pady=10,ipadx=100)
root.mainloop()