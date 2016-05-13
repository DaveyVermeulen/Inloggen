from tkinter import *
from datetime import datetime
import time
import json

#Eigen modules
import Scripts_GUI

#Keuze tussen modus
class App:
    def __init__(self, root):

        #Maak frame1 voor algemene informatie
        frame1 = Frame(root, bg="#111111")
        frame1.pack()

        #Informatie in frame1
        info = Label(frame1, text='Welkom bij het inkloksysteem van het Technasium \n' 'Kies hieronder de modus', bg="#111111", fg="white")
        info.pack(padx=5, pady=5)
        #Maak frame2 voor buttons
        frame2 = Frame(root)
        frame2.pack()
           
        #button1 in frame2 voor database
        def data():
            root.destroy()
            Scripts_GUI.database()
    
        button1 = Button(frame1, text='Database', bg="#000033", fg="white", command=data)
        button1.pack(side=RIGHT, padx=5, pady=5)

        #button2 in frame2 voor inklokken
        def klok():
            root.destroy()
            Scripts_GUI.inklokken()

        button2 = Button(frame1, text='Inklokken', bg="#000033", fg="white", command=klok)
        button2.pack(side=RIGHT)

root = Tk()
root.title("Inkloksysteem 5A OeO")          
app = App(root)
root.mainloop()
