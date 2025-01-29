from tkinter import *
from tkinter import messagebox

def search():
    query = search_entry.get()
    if query:
        messagebox.showinfo("Search",f"You searched for: {query}")
    else:
        messagebox.showwarning("Search","Please enter a search term.")    

def course_selected(selected_course):
    messagebox.showinfo("Course Selected", f"You selected: {selected_course}")

def populate_table(selected_course):
    # Clear the table before populating new data
    for widget in table_frame.winfo_children():
        widget.destroy()

    # Add table headers
    headers = ["SN", "Course", "Username", "Score", "", "", ""]
    for col, header in enumerate(headers):
        Label(table_frame, text=header, font=("Arial", 12, "bold"), bg="lightgrey", width=12).grid(row=0, column=col, padx=1, pady=1)

    # Populate table rows with dummy data
    data = [
        [1, selected_course, "User1", "90",],
        [2, selected_course, "User2", "85",],
        [3, selected_course, "User3", "75",],
        [4, selected_course, "User4", "80",],
    ]

    for row_idx, row_data in enumerate(data):
        for col_idx, value in enumerate(row_data):
            Label(table_frame, text=value, font=("Arial", 12), bg="white", width=12, relief="ridge").grid(row=row_idx + 1, column=col_idx, padx=1, pady=1)



root=Tk()
root.geometry('1000x800')

root.title('Leaderboard')
              
mainframe= Frame(root, bd=2, relief="ridge")
mainframe.place(x=0,y=0,width=1000, height=800)

 
topfr= Frame(root, bd=2, relief="ridge")  
topfr.place(x=0, y=0, width=1000, height=70)   
Label(topfr, text="LEADERBOARD", font=("Arial", 30, "bold"),fg='black').place(x=500,y=0)

bottomfr= Frame(root, bd=2, relief="ridge")  
bottomfr.place(x=370, y=60, width=600, height=60)   
Label(bottomfr, text="FINAL STANDING", font=("Arial", 23, "bold"),fg='black').place(x=145,y=10)
       
searchfr = Frame(root, bd=2, relief="ridge", bg="lightgrey")
searchfr.place(x=0, y=250, width=300, height=50)

Label(searchfr, font=("Arial", 14), bg="lightgrey").place(x=10, y=30)
search_entry = Entry(searchfr, width=15, font=("Arial", 14))
search_entry.place(x=90, y=8)

search_button = Button(searchfr, text="Search", font=("Arial", 12), command=search)
search_button.place(x=10, y=3)

cos= OptionMenu(master=None,variable=int,value=str)
cos.place(x=330,y=250, width=200,height=45)

course_frame = Frame(root, bd=2, relief="ridge", bg="lightgrey")
course_frame.place(x=330, y=250, width=280, height=50)

Label(course_frame, font=("Arial", 12), bg="lightgrey").place(x=10, y=10)

courses = ["Loksewa", "CEE", "IOE", "Driving"]
selected_course = StringVar(value="Choose course")

course_menu = OptionMenu(course_frame, selected_course, *courses, command=course_selected)
course_menu.config(font=("Arial", 10), width=20)
course_menu.place(x=25, y=5)


date_frm = Entry(width=15, font=('Arial',14))
date_frm.place(x=770,y=200)

Label(text="From:",font=('Arial',14),).place(x=700,y=200)

date_to = Entry(width=15, font=('Arial',14))
date_to.place(x=770,y=250)

Label(text="To:",font=('Arial',14),).place(x=728,y=250)

table_frame = Frame(root, bd=2, relief="ridge", bg="lightgrey")
table_frame.place(x=150,y=400, width=660, height=200)

populate_table("Loksewa")

root.mainloop()