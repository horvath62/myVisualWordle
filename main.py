

import tkinter as tk
#from tkinter import ttk
from myClass import *

# ROWS and COLUMNS (GLOBAL)
rows=7
cols=6

wordfile_20k = "fiveletter_20k_trimmed.txt"
# wordfile_20k = "fiveletter_test.txt"
wordfile_71k = "fiveletter_71k.txt"
# wordfile_71k = "fiveletter_test.txt"

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

    nextcell()

    updateresults()

    currentcol = c
    currentrow = r
    nextcell()

    #print('button: current(',r,',',c,') color:', bgcolor, cmap(bgcolor))
    #printcells(rows,cols,cell)


def keydown(e):
    global currentcol, currentrow
    # print("keydown: current(",currentrow,',',currentcol,')',e.char)

def keyup(e):
    global currentcol, currentrow
    print("keyup:","current(",currentrow,',',currentcol,')',e.char)
    letter = e.char.upper()
    if len(letter) == 0:
        # non character (backspace, etc..)
        print("non-character: current cell:(", currentrow, ',', currentcol, ')')
        cell[currentrow][currentcol].setletter(' ')
        btn[currentrow][currentcol].config(text=' ')

    elif (ord(letter) <= 90 and ord(letter) >= 65) or (ord(letter) == 32):
        # letter or space
        cell[currentrow][currentcol].setletter(letter)
        btn[currentrow][currentcol].config(text=letter)
        nextcell()
        updateresults()
        print("keyup:", "new current(", currentrow, ',', currentcol, ')')

    else:
        # not a letter (!@#$ etc...)
        print("NOT A LETTER: current(", currentrow, ',', currentcol, ')', letter)
        cell[currentrow][currentcol].setletter(' ')
        btn[currentrow][currentcol].config(text=' ')

def nextcell():
    # increment to next cell
    global currentcol, currentrow
    if currentcol < cols - 1:
        currentcol += 1
    else:        # last column
        if currentrow < rows - 1:
            currentrow += 1
            currentcol = 0
        else:    # last row
            currentcol = cols - 1


def updateresults():

    # CREATE SEARCH CRITERIA
    crit.scanwords(rows,cols,cell)
    crit.printrowlist()
    crit.makecriteria()
    crit.mergecriteria()

    # APPLY SEARCH CRITERIA TO WORDLISTS
    wr20k.criteriaresults(w20k.words, crit.mergecrit, cols)
    text20k = wr20k.formatwords(16,160)
    wr71k.criteriaresults(w71k.words, crit.mergecrit, cols)
    wr71k.words = wr71k.uniquewords(wr20k.words)
    text71k = wr71k.formatwords(16, 160)
    # print(text20k+text71k)
    bottomlabel.config(text=text20k+text71k)

    # DISPLAY RESULTS
    # crit.textcriteria()
    # sidelabel.config(text=crit.strcrit+crit.strerror)
    text20freq = wr20k.letterfrequency(cols)
    sidelabel.config(text=text20freq)

    text20score = wr20k.wordscore(cols)
    # print(text20score)
    side2label.config(text=text20score)

    text20double = wr20k.doublescore(cols)
    # print(text20double)
    side3label.config(text=text20double)



def backspace(e):
    # Note after this routine, the default keyrelease(keyup) will run
    global currentcol, currentrow
    print("backspace: old current(",currentrow,',',currentcol,')')
    if currentcol > 0:
        currentcol -= 1
    elif currentrow > 0:
        currentrow -= 1
        currentcol = cols - 1
    print("backspace: new current(",currentrow,',',currentcol,')')



def focus(event):
    widget = ws.focus_get()
    # print("focus:", widget, " has focus")


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

sidelabeltext = 'Wordle Helper Program.\nClick cell to change color'
sidelabel = tk.Label(ws, text=sidelabeltext, width=40, height=28, bd=2,
                     font=('Courier',8,'bold'), justify='left', anchor="nw" )
sidelabel.grid(row=0,column=cols+1, rowspan=rows)

side2labeltext = 'Word score'
side2label = tk.Label(ws, text=side2labeltext, width=20, height=28, bd=2,
                     font=('Courier',8,'bold') ,justify='left', anchor="nw" )
side2label.grid(row=0,column=cols+2, rowspan=rows)

side3labeltext = 'Double Letter'
side3label = tk.Label(ws, text=side3labeltext,width=20, height=28, bd=2,
                     font=('Courier',8,'bold'),justify='left', anchor="nw" )
side3label.grid(row=0,column=cols+3, rowspan=rows)



bottomlabeltext = 'Search Results'
bottomlabel = tk.Label(ws, text=bottomlabeltext,width=100, height=42, bd=2,
                       font=('Courier',10,'bold'),justify='left', anchor="nw" )
bottomlabel.grid(row=rows, column=0, columnspan=cols+4)



ws.mainloop()