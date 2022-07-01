

import tkinter as tk
#from tkinter import ttk
from myClass import *


global currentrow
global currentcol



def b11callback():
    print("b11callback:")
    b11bg = button11.cget('bg')
    if b11bg == "green":
        button11.config(bg="red")
    else:
        button11.config(bg="green")

    button11.focus_set()


def btncallback(r,c):
    #bgcolor = btn[r][c].cget('bg')
    bgcolor = cell[r][c].nextcolor()
    btn[r][c].config(bg=bgcolor)

    #btn[r][c].config(bg='red')
    print("btncallback:",r,c, bgcolor)

def keydown(e):
    print("keydown:",e.char)
    #focus_widget = ws.focus_get()
    #focus_widget.config(bg='white')
    #focus_widget.config(text=e.char)
    #print(focus_widget.cget('bg'))
    #button11.config(text=e.char)

def keyup(e):
    global currentcol, currentrow
    print("keyup:",e.char)
    cell[currentrow][currentcol].setletter(e.char)
    btn[currentrow][currentcol].config(text=e.char)

    if currentcol < cols-1:
        currentcol += 1
    else:
        currentcol = 0
        if currentrow < rows - 1:
            currentrow += 1


def focus(event):
    widget = ws.focus_get()
    print("focus:", widget, " has focus")


ws = tk.Tk()
ws.title("Wordle Helper")
ws.resizable(False,False)
ws.geometry('800x800')
ws.configure(bg='gray')
#ws.bind("<KeyPress>", keydown)
#ws.bind("<KeyRelease>", lambda event, arg=3: keyup(event,arg))
ws.bind("<KeyRelease>", keyup)

ws.bind_all("<Button-1>", lambda e: focus(e))

currentrow = 0
currentcol = 0

rows=6
cols=5

cell = [[0 for x in range(cols)] for y in range(rows)]
btn = [[0 for x in range(cols)] for y in range(rows)]
for r in range(rows):
    for c in range(cols):
        cell[r][c] = LetterCell(r,c,"")
        btn[r][c] = tk.Button(ws, text=cell[r][c].letter, command=lambda r=r, c=c : btncallback(r,c),
                              font=('calibre',20,'bold'), fg='white', justify='center', width=2,bg=cell[r][c].color)
        btn[r][c].grid(row=r, column=c)



r = 1
c = 1

ws.mainloop()