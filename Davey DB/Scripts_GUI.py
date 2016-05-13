from tkinter import *
from datetime import datetime
import time
import json

def database():
    class Database:
        def __init__(self, root):

            #Maak frame1 voor algemene informatie
            frame1 = Frame(rootDB, bg="#111111")
            frame1.pack()

            #Informatie in frame1
            info = Label(frame1, text='Vul hieronder het leerlingnummer in \n' 'of scan de schoolpas', bg="#111111", fg="white")
            info.pack(padx= 10, pady=10)

            #Maak frame2 voor tekstvak en button 
            frame2 = Frame(rootDB, bg="#111111")
            frame2.pack()
            
            #Tekstvak
            def focus(event):               #verwijder text bij input
                text.delete(0, END)

            text = Entry(frame2)
            text.insert(0, "Typ hier..")
            text.bind("<FocusIn>", focus)   #verwijder text bij input
            text.pack(side=LEFT, padx=5, pady=5)

            #ButtonE voor verzenden input
            def enter():
                ln=text.get()
                text.delete(0, END)
                print(ln)
                
            buttonE = Button(frame2, text='Enter', bg="#000033", fg="white", command=enter)
            buttonE.pack(side=RIGHT, padx=5, pady=5)

    rootDB = Tk()
    rootDB.title('Database Mondial College Lindenholt')
    app = Database(rootDB)
    rootDB.mainloop()
        
"""def inklokken():

    inlog = {}
    Leerlingen = json.load(open('database.txt'))
    ln = input("Vul je leerlingennummer in: ")
    while ln:
        naam = Leerlingen.get(ln, "None")
        if naam == "None":
            print("Leerling onbekend, probeer opnieuw")
        else:
            print("Welkom", naam)
            tijd = datetime.now()
            print("het is vandaag", '%s-%s' % (tijd.day, tijd.month))
            print("Tijd:", '%s:%s:%s' % (tijd.hour, tijd.minute, tijd.second))
            inlog[naam] = (tijd.hour*3600 + tijd.minute*60 + tijd.second)
            json.dump(inlog, open('inkloktijd.txt', 'w'))
        time.sleep(2)
        ln = input("Vul je leerlingennummer in: ")
    print("Systeem zal nu afsluiten")
"""

