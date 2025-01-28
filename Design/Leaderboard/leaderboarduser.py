from tkinter import *

def create_table(frame, data):

    headers = ["SN", "Username", "Score"]
    for col, header in enumerate(headers):
        Label(frame, text=header, font=("Arial", 12, "bold"), bg="lightgrey", width=10).grid(row=0, column=col, padx=1, pady=1)

    for row_idx, row_data in enumerate(data):
        for col_idx, value in enumerate(row_data):
            Label(frame, text=value, font=("Arial", 12), bg="white", width=10, relief="ridge").grid(row=row_idx + 1, column=col_idx, padx=1, pady=1)

root = Tk()
root.geometry('1000x800')
root.title('Quiz Leaderboard')

mainframe = Frame(root, bd=2, relief="ridge")
mainframe.place(x=0, y=0, width=1000, height=800)

topfr = Frame(root, bd=2, relief="ridge")
topfr.place(x=0, y=0, width=1000, height=70)
Label(topfr, text="LEADERBOARD", font=("Arial", 30, "bold"), fg='black').place(x=500, y=0)

bottomfr = Frame(root, bd=2, relief="ridge")
bottomfr.place(x=370, y=60, width=600, height=60)
Label(bottomfr, text="FINAL STANDING", font=("Arial", 23, "bold"), fg='black').place(x=145, y=10)


data = {
    "Loksewa": [
        [1, "User1", "90"],
        [2, "User2", "85"],
        [3, "User3", "75"],
        [4, "User4", "65"],
        [5, "User5", "60"],
        [6, "User6", "55"],
    ],
    "CEE": [
        [1, "User5", "95"],
        [2, "User6", "88"],
        [3, "User7", "78"],
        [4, "User8", "82"],
        [5, "User5", "60"],
        [6, "User6", "55"],
    ],
    "IOE": [
        [1, "User9", "92"],
        [2, "User10", "87"],
        [3, "User11", "77"],
        [4, "User12", "81"],
        [5, "User5", "60"],
        [6, "User6", "55"],
    ],
    "Driving": [
        [1, "User13", "89"],
        [2, "User14", "84"],
        [3, "User15", "74"],
        [4, "User16", "79"],
        [5, "User5", "60"],
        [6, "User6", "55"],
    ],
}

table_frame1 = Frame(root, bd=2, relief="ridge", bg="lightgrey")
table_frame1.place(x=40, y=190, width=400, height=250)
Label(root, text="Loksewa", font=('Arial', 14, 'bold'), fg='black').place(x=180, y=165)
create_table(table_frame1, data["Loksewa"])

table_frame2 = Frame(root, bd=2, relief="ridge", bg="lightgrey")
table_frame2.place(x=550, y=190, width=400, height=250)
Label(root, text="CEE", font=('Arial', 14, 'bold'), fg='black').place(x=730, y=165)
create_table(table_frame2, data["CEE"])

table_frame3 = Frame(root, bd=2, relief="ridge", bg="lightgrey")
table_frame3.place(x=40, y=525, width=400, height=250)
Label(root, text="IOE", font=('Arial', 14, 'bold'), fg='black').place(x=180, y=500)
create_table(table_frame3, data["IOE"])

table_frame4 = Frame(root, bd=2, relief="ridge", bg="lightgrey")
table_frame4.place(x=550, y=525, width=400, height=250)
Label(root, text="Driving", font=('Arial', 14, 'bold'), fg='black').place(x=700, y=500)
create_table(table_frame4, data["Driving"])

root.mainloop()