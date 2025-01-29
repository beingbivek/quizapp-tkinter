from tkinter import *

root = Tk()
root.title("Circle in Tkinter")
root.geometry("1000x800")  

user = ['Mukesh Babu Acharya','Babu.net','9862148844','babu@gmail.com']

mainframe= Frame(root, bd=2, relief="ridge")
mainframe.place(x=0,y=0,width=1000, height=800)

secframe= Frame(root, bd=2, relief='ridge')
secframe.place(x=50,y=50,width=900, height=700)

root.title('User Profile')

canvas = Canvas(root, width=250, height=250,)
canvas.place(x=350,y=70)

Label( text=user[1],font=('Arial',12,'bold')).place(x=436,y=275)

Label(root, text="Name",).place(x=70, y=320)
name_entry = Entry(root,width=35)
name_entry.place(x=70, y=340)
name_entry.insert(0,user[0])

Label(root, text="User Name",).place(x=70, y=400)
usrname_entry = Entry(root,width=35)
usrname_entry.place(x=70, y=420)
usrname_entry.insert(0,user[1])

Label(root, text="Contact Number",).place(x=70, y=480)
cnt_entry = Entry(root,width=35)
cnt_entry.place(x=70, y=500)
cnt_entry.insert(0,user[2])


Label(root, text="Email",).place(x=70, y=560)
email_entry = Entry(root,width=35)
email_entry.place(x=70, y=580)
email_entry.insert(0,user[3])

Label(root, text="New Password",).place(x=640, y=320)
pass_entry = Entry(root,width=35)
pass_entry.place(x=640, y=340)

Label(root, text="Confirm Password",).place(x=640, y=400)
conpass_entry = Entry(root,width=35)
conpass_entry.place(x=640, y=420)

btm1= Button(text='UPDATE',font=('Arial',14,'bold'))
btm1.place(x=83,y=690)

btm1= Button(text='CANCEL',font=('Arial',14,'bold'))
btm1.place(x=800,y=690)


x1, y1 = 80, 80  
x2, y2 = 200, 200  

canvas.create_oval(x1, y1, x2, y2, fill="lightgrey", outline="black",)

root.mainloop()