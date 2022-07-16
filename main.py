

import tkinter as tk
#from tkinter import ttk
from myClass import *

# ROWS and COLUMNS (GLOBAL)
rows=6
cols=5

wordfile_20k = "fiveletter_20k_trimmed.txt"
# wordfile_20k = "fiveletter_test.txt"
wordfile_71k = "fiveletter_71k.txt"

# Make list of five letter words
w20k = Wordlist([], "20K WORD FILE")
w20k.readwordfile(wordfile_20k)
wr20k = Wordlist([],'Results from 20K wordlist')

w71k = Wordlist([], "71K WORD FILE")
w71k.readwordfile(wordfile_71k)
wr71k = Wordlist([],'Results from 71K wordlist')


crit = Criteria(cols)



def button(r,c):
    global currentcol, currentrow
    bgcolor = cell[r][c].nextcolor()
    btn[r][c].config(bg=cmap(bgcolor))
    #currentcol = c
    #currentrow = r
    #print('button: current(',r,',',c,') color:', bgcolor, cmap(bgcolor))

    #printcells(rows,cols,cell)

    #crit.scanwords(rows,cols,cell)
    #crit.printrowlist()
    #crit.printrow(0)
    #crit.makecriteria(0)

def keydown(e):
    global currentcol, currentrow
    print("keydown: current(",currentrow,',',currentcol,')',e.char)

def keyup(e):
    global currentcol, currentrow
    print("keyup:","current(",currentrow,',',currentcol,')',e.char)
    letter = e.char.upper()
    # print ("upper", letter, ord(letter))
    if len(letter) == 0:
        # non character
        print("non-character: current(", currentrow, ',', currentcol, ')')
        cell[currentrow][currentcol].setletter(' ')
        btn[currentrow][currentcol].config(text=' ')

    elif ord(letter) > 90 or ord(letter) < 65:
        # not a letter
        print("NOT A LETTER: current(", currentrow, ',', currentcol, ')', letter)
        cell[currentrow][currentcol].setletter(' ')
        btn[currentrow][currentcol].config(text=' ')
    else:
        cell[currentrow][currentcol].setletter(letter)
        btn[currentrow][currentcol].config(text=letter)

        # increment to next cell
        if currentcol < cols-1:
            currentcol += 1
        else:
            currentcol = 0
            if currentrow < rows - 1:
                currentrow += 1
        print("increment:", "current(", currentrow, ',', currentcol, ')')

    # CREATE SEARCH CRITERIA
    crit.scanwords(rows,cols,cell)
    crit.printrowlist()
    crit.makecriteria()
    crit.mergecriteria()
    crit.textcriteria()
    sidelabel.config(text=crit.strcrit+crit.strerror)

    # APPLY SEARCH CRITERIA TO 20K WORDLIST
    wr20k.criteriaresults(w20k.words, crit.mergecrit)
    wr20k.printwords(10,100)
    bottomlabel.config(text=wr20k.words)
    wr71k.criteriaresults(w20k.words, crit.mergecrit)
    wr71k.printwords(10,100)


def backspace(e):
    # Note after this routine, the default keyrelease(keyup) will run
    global currentcol, currentrow
    print("backspace: current(",currentrow,',',currentcol,')')
    if currentcol > 0:
        currentcol -= 1
    elif currentrow > 0:
        currentrow -= 1
        currentcol = 4


def focus(event):
    widget = ws.focus_get()
    print("focus:", widget, " has focus")


def scancells():
    for rindex in range(rows):
        word = ">>>"
        color = ">>>"
        for cindex in range(cols):
            word += cell[rindex][cindex].letter
            color += cell[rindex][cindex].color
        word += "<<<"
        color += "<<<"
        print(currentrow, currentcol, rindex, cindex, word, color)




ws = tk.Tk()
ws.title("Wordle Helper")
ws.resizable(False,False)
ws.geometry('800x800')
ws.configure(bg='gray')
# ws.bind("<KeyPress>", keydown)
ws.bind("<KeyRelease>", keyup)
ws.bind("<BackSpace>", backspace)


ws.bind_all("<Button-1>", lambda e: focus(e))

currentrow = 0
currentcol = 0

cell = [[0 for x in range(cols)] for y in range(rows)]
btn = [[0 for x in range(cols)] for y in range(rows)]
for r in range(rows):
    for c in range(cols):
        cell[r][c] = LetterCell(r,c," ")
        btn[r][c] = tk.Button(ws, text=cell[r][c].letter, command=lambda r=r, c=c : button(r,c),
                              font=('calibre',20,'bold'), fg='white', justify='center', width=2,
                              bg=cmap(cell[r][c].color)
                              )
        btn[r][c].grid(row=r, column=c)

sidelabel = tk.Label(ws, text="",width=70, height=20, bd=0,
                     font=('calibre',10,'bold'),justify='left', anchor="nw" )
sidelabel.grid(row=0,column=cols+1, rowspan=rows)

bottomlabel = tk.Label(ws, text="",width=100, height=35, bd=0,
                       font=('calibre',10,'bold'),justify='left', anchor="nw" )
bottomlabel.grid(row=rows, column=0, columnspan=cols+2)



ws.mainloop()