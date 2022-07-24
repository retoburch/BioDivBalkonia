#dropdown Menu
from tkinter import *

root = Tk()
root.geometry("200x200")

def show():
    label.config(text=clicked.get())

options = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

clicked = StringVar()
clicked.set("Monday")

drop = OptionMenu(root, clicked, *options)
drop.pack()

button = Button(root, text="click Me", command=show).pack()

label = Label(root, text=" ")
label.pack()

root.mainloop()

#get input with tkinter
from tkinter import *

ws = Tk()
ws.title("PythonGuides")
ws.geometry('400x300')
ws['bg'] = '#ffbf00'

def printValue():
    pname = player_name.get()
    Label(ws, text=f'{pname}, Registered!', pady=20, bg='#ffbf00').pack()


player_name = Entry(ws)
player_name.pack(pady=30)

Button(
    ws,
    text="Register Player",
    padx=10,
    pady=5,
    command=printValue
    ).pack()

ws.mainloop()

