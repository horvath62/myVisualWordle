

import tkinter as tk
#from tkinter import ttk
from myClass import *


# ROWS and COLUMNS (GLOBAL)
rows=5
cols=5

notaindex = 0

# debug = True
debug = False

if debug:
    wordfile_20k = "fiveletter_test.txt"
    wordfile_71k = "fiveletter_test.txt"
else:
    wordfile_71k = "fiveletter_71k.txt"
    wordfile_20k = "fiveletter_20k_trimmed.txt"

wordfile_not = "fiveletter_notaword.txt"


# INIT Wordlist objects of five letter words
w20k = Wordlist([], "20K WORD FILE")
w20k.readwordfile(wordfile_20k)
wr20k = Wordlist([],'Results from 20K wordlist')

w71k = Wordlist([], "71K WORD FILE")
w71k.readwordfile(wordfile_71k)
wr71k = Wordlist([],'Results from 71K wordlist')

wAll = Wordlist([], "Merged Word Files")
wrAll = Wordlist([], 'Results from All Words')

wNota = Wordlist([], "Not A Word List")
wNota.readwordfile(wordfile_not)
wrNota = Wordlist([],'Criteria Results of Not a Word List')

wr20kG = Wordlist([], "Elimination Green Wordlist")
wr20kGY = Wordlist([], "Elimination all Letters Green and Yellow")



# Init search criteria
crit = Criteria(cols)
# elimGcrit = Criteria(cols)
# noColorcrit = Criteria(cols)

def button(r,c):
    print(">>>BUTTON<<<")
    global currentcol, currentrow
    bgcolor = cell[r][c].nextcolor()
    btn[r][c].config(bg=cmap(bgcolor))

    #nextcell()

    updateresults()

    #currentcol = c
    #currentrow = r
    #nextcell()

    #print('button: current(',r,',',c,') color:', bgcolor, cmap(bgcolor))
    #printcells(rows,cols,cell)

def press_notaword():
    print(">>>NOT A WORD<<<")
    #if not in list then add to list
    theword = notaword['text']
    if wNota.checkWord(theword):
        #remove word from Notaword list
        wNota.removeword(theword)
        notaword.config(bg='green')
    else:
        #addword
        wNota.addword(theword)
        notaword.config(bg='red')

    updateresults()
def press_notanext():
    print(">>>NEXT WORD<<<")
    global notaindex
    totalwords = wrAll.getWordcount()
    notaindex += 1
    if notaindex > totalwords - 1:
        notaindex = 0
    notaword_shown = wrAll.getWord(notaindex)
    notaword.config(text=notaword_shown)
    if wrAll.checkWord(notaword_shown):
        notaword.config(bg='green')
    else:
        notaword.config(bg='red')
    updateresults()

def press_notaprev():
    print(">>>PREV WORD<<<")
    global notaindex
    totalwords = wrAll.getWordcount()
    notaindex -= 1
    if notaindex < 0:
        notaindex = totalwords - 1
    notaword_shown = wrAll.getWord(notaindex)
    notaword.config(text=notaword_shown)
    if wrAll.checkWord(notaword_shown):
        notaword.config(bg='green')
    else:
        notaword.config(bg='red')
    updateresults()

def press_notawrite():
    wNota.writewordfile(wordfile_not)

def keydown(e):
    global currentcol, currentrow
    # print(">>>EVENT<<< keydown: current(",currentrow,',',currentcol,')',e.char)

def keyup(e):
    global currentcol, currentrow
    print(">>>EVENT<<< keyup:","current(",currentrow,',',currentcol,')',e.char)
    letter = e.char.upper()
    if len(letter) == 0:
        # non character (backspace, etc..)
        print("   keyup: non-character")
        cell[currentrow][currentcol].setletter(' ')
        btn[currentrow][currentcol].config(text=' ')
        updateresults()

    elif (ord(letter) <= 90 and ord(letter) >= 65) or (ord(letter) == 32):
        # letter or space
        cell[currentrow][currentcol].setletter(letter)
        btn[currentrow][currentcol].config(text=letter)
        nextcell()
        updateresults()
        print("   keyup: letter",letter)

    else:
        # not a letter (!@#$ etc...)
        print("   keyup: NOT A LETTER", letter)
        cell[currentrow][currentcol].setletter(' ')
        btn[currentrow][currentcol].config(text=' ')

def nextcell():
    # increment to next cell
    # print("NEXT CELL")
    global currentcol, currentrow
    btn[currentrow][currentcol].config(bg="black")
    if currentcol < cols - 1:
        currentcol += 1
    else:        # last column
        if currentrow < rows - 1:
            currentrow += 1
            currentcol = 0
        else:    # last row
            currentcol = cols - 1
    btn[currentrow][currentcol].config(bg="grey")
    # print("   new cell(", currentrow, ',', currentcol, ')')

def backspace(e):
    # Note after this routine, the default keyrelease(keyup) will run
    global currentcol, currentrow
    btn[currentrow][currentcol].config(bg="black")
    print(">>>EVENT: Backspace<<<: old current(",currentrow,',',currentcol,')')
    if currentcol > 0:
        currentcol -= 1
    elif currentrow > 0:
        currentrow -= 1
        currentcol = cols - 1
    btn[currentrow][currentcol].config(bg="grey")
    # print("   backspace: new current(",currentrow,',',currentcol,')')

def focus(event):
    widget = ws.focus_get()
    print(">>>Focus<<<", widget, " has focus")

def scancells():
    for rindex in range(rows):
        word = ">>>"
        color = ">>>"
        for cindex in range(cols):
            word += cell[rindex][cindex].letter
            color += cell[rindex][cindex].color
        word += "<<<"
        color += "<<<"
        # print("   ",currentrow, currentcol, rindex, cindex, word, color)




def updateresults():
    print("UPDATE RESULTS")
    global rows, cols
    # CREATE SEARCH CRITERIA
    crit.scanwords(rows,cols,cell)
    # crit.printrowlist()
    crit.makecriteria()
    crit.mergecriteria()
    crit.printcriteria()

    # APPLY SEARCH CRITERIA TO WORDLISTS
    wr20k.criteriaresults(w20k.words, crit.mergecrit, cols)
    text20k = wr20k.formatwords(16, 64)
    wr71k.criteriaresults(w71k.words, crit.mergecrit, cols)
    wr71k.words = wr71k.wordssubtract(wr20k.words)
    text71k = wr71k.formatwords(16, 64)
    # print(text20k+text71k)

    wrNota.criteriaresults(wNota.words, crit.mergecrit, cols)
    textNota = wrNota.formatwords(16, 64)

    wrAll.words = wr20k.wordsmerge(wr71k.words)
    wrAll.words = wrAll.wordssubtract(wrNota.words)
    textAll = wrAll.formatwords(16, 64)

    # find all green letters in crit, put in self.greenletters list
    crit.greenletter()

    wAll.words = w20k.wordsmerge(w71k.words)


    # DISPLAY RESULTS
    bottomlabel.config(text=text20k + text71k + textAll + textNota)
    # + textelimG + textnoColor

    #textfreq = wr20k.letterfrequency(cols)
    #sidelabel.config(text=textfreq)

    #text20score = wr20k.wordscore(cols)
    #side2label.config(text=text20score)

    textAllfreq = wrAll.letterfrequency(cols)
    sidelabel.config(text=textAllfreq)

    textAllscore = wrAll.wordscore(cols)
    side2label.config(text=textAllscore)

    textNoGreenscore = wAll.scorewords_noG(crit.greenletters, wrAll, cols)
    side3label.config(text=textNoGreenscore)

    # textelimG = wr20k.elimGscore(wr20k, cols)
    # side4label.config(text=textelimG)

    for c in range(cols):
        for r in range(rows):
            color = cell[r][c].color
            if color != 'B':
                btn[r][c].config(bg=cmap(color))


# SETUP TK GRAPHICS
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

# The button should really be a class.
# one forum said fields are better than buttons...????
cell = [[0 for x in range(cols)] for y in range(rows)]
btn = [[0 for x in range(cols)] for y in range(rows)]
btnlast = [ 0 for x in range(cols)]
for r in range(rows):
    for c in range(cols):
        cell[r][c] = LetterCell(r,c," ")
        btn[r][c] = tk.Button(ws, text=cell[r][c].letter, command=lambda r=r, c=c: button(r,c),
                              font=('calibre',20,'bold'), fg='white', justify='center', width=2,
                              bg=cmap(cell[r][c].color)
                              )
        btn[r][c].grid(row=r, column=c)

notaword = tk.Button(ws, text='ABCDE', command=lambda: press_notaword(),
                          font=('calibre', 20, 'bold'), fg='white', justify='center', width=5,
                          bg=cmap('B')
                          )
notaword.grid(row=rows, column=0, columnspan=2)

notanext = tk.Button(ws, text='+', command=lambda: press_notanext(),
                          font=('calibre', 20, 'bold'), fg='white', justify='center', width=2,
                          bg=cmap('B')
                          )
notanext.grid(row=rows, column=2)

notaprev = tk.Button(ws, text='-', command=lambda: press_notaprev(),
                          font=('calibre', 20, 'bold'), fg='white', justify='center', width=2,
                          bg=cmap('B')
                          )
notaprev.grid(row=rows, column=3)

notawrite = tk.Button(ws, text='W', command=lambda: press_notawrite(),
                          font=('calibre', 20, 'bold'), fg='white', justify='center', width=2,
                          bg=cmap('B')
                          )
notawrite.grid(row=rows, column=4)


sidelabeltext = 'Wordle Helper Program.\nClick cell to change color'
sidelabel = tk.Label(ws, text=sidelabeltext, width=40, height=28, bd=2,
                     font=('Courier',8,'bold'), justify='left', anchor="nw" )
sidelabel.grid(row=0,column=cols+1, rowspan=rows+1)

side2labeltext = 'Word score'
side2label = tk.Label(ws, text=side2labeltext, width=14, height=28, bd=2,
                     font=('Courier',8,'bold') ,justify='left', anchor="nw" )
side2label.grid(row=0,column=cols+2, rowspan=rows+1)

side3labeltext = 'NO GREEN'
side3label = tk.Label(ws, text=side3labeltext,width=12, height=28, bd=2,
                     font=('Courier',8,'bold'),justify='left', anchor="nw" )
side3label.grid(row=0,column=cols+3, rowspan=rows+1)

side4labeltext = 'ELIMINATION'
side4label = tk.Label(ws, text=side4labeltext,width=12, height=28, bd=2,
                     font=('Courier',8,'bold'),justify='left', anchor="nw" )
side4label.grid(row=0,column=cols+4, rowspan=rows+1)



bottomlabeltext = 'Search Results'
bottomlabel = tk.Label(ws, text=bottomlabeltext,width=100, height=42, bd=2,
                       font=('Courier',10,'bold'),justify='left', anchor="nw" )
bottomlabel.grid(row=rows+1, column=0, columnspan=cols+5)



ws.mainloop()