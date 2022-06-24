

#https://stackoverflow.com/questions/18471886/how-to-create-an-array-of-multiple-tkinter-scale-widgets-with-python



import tkinter as tk
from tkinter import ttk

ws = tk.Tk()
ws.title("Wordle Helper")
ws.resizable(False,False)
ws.geometry('800x800')
ws.configbg=('#88F04')

char11 = tk.StringVar()
char12 = tk.StringVar()

char11.set("A")
char12.set("B")


box11 = ttk.Entry(ws, textvariable=char11, font=('calibre',20,'bold'), justify='center', width=2, foreground='green' ).place(x=5, y=5)
box12 = ttk.Entry(ws, textvariable=char12).place(x=50, y=50)
#box11.pack(expand=True)
#box11.insert('end', message)



#box11 = ttk





ws.mainloop()