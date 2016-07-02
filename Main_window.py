from tkinter import *
from tkinter import ttk
import pymysql
import time
from datetime import datetime
import decimal
from easygui import *

try:
    import Scripts as kx
except:
    from Inklokken import Scripts as kx

state = open("/home/pi/Desktop/Inklokken/update.txt", "w")
state.write("Yes")
    
def start():
    root = Tk()
    root.title("THE KRIP")

    frame1 = Frame(root, width=500, height=600, bg="black")
    frame1.pack(side=LEFT, padx=5, pady=5)
    
    logo = PhotoImage(file="/home/pi/Desktop/Inklokken/logo_school.gif")
    labelF = Label(frame1, image=logo)
    
    labelF.image = logo #Bewaar foto zodat deze niet verwijderd wordt in cleanup
    labelF.pack(padx=5, pady=5)
    
    button1 = Button(frame1, text="Uitklokken", bg="#000033", fg="white", command = kx.uitKlok)
    button1.pack(side=BOTTOM, padx=5, pady=5)
    
    frame2 = Frame(root, width=800, height=700, bg="black")
    frame2.pack(side=RIGHT, padx=5)
    
    tree = ttk.Treeview(frame2)
    tree['show'] = 'headings'
    tree["columns"]=("Naam","Leerlingnummer")
    tree.column("Naam", width=500 )
    tree.column("Leerlingnummer", width=300)
    tree.heading("Naam", text="Naam")
    tree.heading("Leerlingnummer", text="Leerlingnummer")
    
    def update():
        db = pymysql.connect(host="localhost", port=3141, user="python", passwd="admin", db="inklokken")
        cur = db.cursor()
        
        state = open("/home/pi/Desktop/Inklokken/update.txt", "r")
        text = state.read()
        if text == "Yes":
            cur.execute("SELECT `Naam`, `Leerlingnummer` FROM `Inkloktijd`")
            info = cur.fetchall()
            state.close()
            state = open("/home/pi/Desktop/Inklokken/update.txt", "w")
            try:
                tree.delete(*tree.get_children())
            except:
                None

            for i in range(0, len(info)):
                print(i)
                tree.insert("", i, text=i+1, values = ((info[i])[0], (info[i])[1]))

            state.write("No")
            state.close()
            db.close()
            root.after(1000, update)
                

        else:
            state.close()
            db.close()
            root.after(1000, update)
                
    tree.pack()
    root.after(1000, update)
    root.mainloop()

start()
