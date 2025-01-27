import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg

win = tk.Tk()
label_frame = ttk.LabelFrame(win,text = 'Contact Details' )

label_frame.grid(row = 0, column=0, padx=40, pady= 10)

name_label = ttk.Label(label_frame,text = 'Enter Name:', font =  ('Helvetica',14))
age_label = ttk.Label(label_frame,text = 'Enter Age:', font =  ('Helvetica',14))
contact_label = ttk.Label(label_frame,text = 'Enter Contact No :', font =  ('Helvetica',14))
email_label = ttk.Label(label_frame,text = 'Enter Email Id :', font =  ('Helvetica',14))
address_label = ttk.Label(label_frame,text = 'Enter Address :', font =  ('Helvetica',14))




name_var = tk.StringVar()
age_var =tk.StringVar()
contact_var = tk.StringVar()
email_var = tk.StringVar()
address_var = tk.StringVar()

name_entry = ttk.Entry(label_frame, width = 36, textvariable = name_var)
age_entry = ttk.Entry(label_frame, width = 36, textvariable= age_var)
contact_entry = ttk.Entry(label_frame, width = 42, textvariable= contact_var)
email_entry = ttk.Entry(label_frame, width= 42, textvariable= email_var)
address_entry = ttk.Entry(label_frame, width= 42, textvariable= address_var)


name_label.grid(row = 0, column= 0, padx = 5, pady = 5, sticky = tk.W)
age_label.grid(row = 0, column = 1, padx =5, pady=5, sticky = tk.W)
contact_label.grid(row = 2, column = 0, padx =5, pady=5, sticky = tk.W)
email_label.grid(row = 3, column = 0, padx =5, pady=5, sticky = tk.W)
address_label.grid(row = 4, column = 0, padx =5, pady=5, sticky = tk.W)


name_entry.grid(row = 1, column = 0, padx=5, pady=5, sticky = tk.W)
age_entry.grid(row=1,column=1,padx=5,pady=5, sticky=tk.W)
contact_entry.grid(row=2,column=1,padx=5,pady=5, sticky=tk.W)
email_entry.grid(row=3,column=1,padx=5,pady=5, sticky=tk.W)
address_entry.grid(row=4,column=1,padx=5,pady=5, sticky=tk.W)


def submit():
  name = name_var.get()
  age = age_var.get()
  contact = contact_var.get()
  email = email_var.get()
  address = address_var.get()
  if name == '' or age == '' or contact == '' or email == '' or address == '' :
    msg.showerror('Error!','Please enter all needed details!')
  else:
    try:
       age = int(age) 
    except ValueError:
        msg.showerror('Error!', 'Only digits are allowed in age!')
    else:
        if age < 18 :
          msg.showwarning("Warning",'You are not allowed!')
          
        elif not contact.isdigit():
           msg.showerror('Error!', 'Only digits are allowed in contact!')
        elif len(contact) != 10:
           msg.showwarning("Warning",'Enter appropriate number!')
           
        elif '@' not in email or '.' not in email :
          msg.showerror('Error!', 'Please include appropriate characters in your email id.')
        else:
          msg.showinfo('Info!',f'''{name}:{age} 
contact No : {contact}
Email id : {email}
Address  : {address} ''')


submit_btn = ttk.Button(label_frame, text ='Submit', command = submit)
submit_btn.grid(row = 5, columnspan=  2, padx = 40)

win.mainloop()

       




