

import tkinter as tk
#from tkinter import ttk
from myClass import *

def b11callback():
    print("b11callback:")
    b11bg = button11.cget('bg')
    if b11bg == "green":
        button11.config(bg="red")
    else:
        button11.config(bg="green")

    button11.focus_set()


def btncallback(r,c):
    bgcolor = btn[r][c].cget('bg')
    if bgcolor == "green":
        btn[r][c].config(bg="red")
    #btn[r][c].config(bg='red')
    print("btncallback:",r,c, bgcolor)




def keydown(e):
    print("keydown:",e.char)
    focus_widget = ws.focus_get()
    #focus_widget.config(bg='white')
    #focus_widget.config(text=e.char)
    print(focus_widget.cget('bg'))
    button11.config(text=e.char)

def keyup(e):
    print("keyup:",e.char)

def focus(event):
    widget = ws.focus_get()
    print("focus:", widget, " has focus")


ws = tk.Tk()
ws.title("Wordle Helper")
ws.resizable(False,False)
ws.geometry('800x800')
ws.configure(bg='gray')
ws.bind("<KeyPress>", keydown)
ws.bind("<KeyRelease>", keyup)

ws.bind_all("<Button-1>", lambda e: focus(e))

button11 = tk.Button(ws, text = "X", command = b11callback, font=('calibre',20,'bold'),justify='center', width=2,bg='green'  )
button12 = tk.Button(ws, text = "X", command = b11callback, font=('calibre',20,'bold'),justify='center', width=2,bg='green'  )

button11.grid(row=7, column=1)
button12.grid(row=7, column=2)

rows=6
cols=5
btn = [[0 for x in range(cols)] for y in range(rows)]
for r in range(rows):
    for c in range(cols):
        btn[r][c] = tk.Button(ws, text=c, command=lambda r=r, c=c : btncallback(r,c), font=('calibre',20,'bold'),justify='center', width=2,bg='green')
        btn[r][c].grid(row=r, column=c)

r = 1
c = 1

ws.mainloop()