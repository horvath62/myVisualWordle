

import tkinter as tk
#from tkinter import ttk
from myClass import *


def btncallback(r,c):
    global currentcol, currentrow
    bgcolor = cell[r][c].nextcolor()
    btn[r][c].config(bg=cmap(bgcolor))
    currentcol = c
    currentrow = r
    print("btncallback:",r,c, bgcolor, cmap(bgcolor))

def keydown(e):
    print("keydown:",e.char)

def keyup(e):
    global currentcol, currentrow
    print("keyup:",e.char)
    letter = e.char.upper()
    #print ("upper", letter, ord(letter))
    if len(letter) == 0:
        #non character
        print('NON CHARACTER')
        if currentcol > 0:
            cell[currentrow][currentcol-1].setletter('')
            btn[currentrow][currentcol-1].config(text='')
            currentcol -= 1
    elif ord(letter) > 90 or ord(letter) < 65:
        #not a letter
        print("NOT A LETTER", len(letter))
    else:
        cell[currentrow][currentcol].setletter(letter)
        btn[currentrow][currentcol].config(text=letter)

        #scan all words entered
        for rindex in range(currentrow+1):
            word = ">>>"
            for cindex in range(cols):
                word += cell[rindex][cindex].letter
            print(currentrow, currentcol, rindex, cindex, word)

        #increment to next cell
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
                              font=('calibre',20,'bold'), fg='white', justify='center', width=2,
                              bg=cmap(cell[r][c].color)
                              )
        btn[r][c].grid(row=r, column=c)

ws.mainloop()