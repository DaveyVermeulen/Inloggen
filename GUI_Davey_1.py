from tkinter import *
from tkinter import ttk
import pymysql
import time

db = pymysql.connect(host="localhost", port=3141, user="python", passwd="admin", db="inklokken")
cur = db.cursor()

state = open("update.txt", "w")
state.write("Yes")

def start():
    root = Tk()
    root.title("THE KRIP")

    tree = ttk.Treeview(root)
    tree['show'] = 'headings'
    tree["columns"]=("Naam","Leerlingnummer")
    tree.column("Naam", width=650 )
    tree.column("Leerlingnummer", width=650)
    tree.heading("Naam", text="Naam")
    tree.heading("Leerlingnummer", text="Leerlingnummer")
    
    def update():
        cur.execute("SELECT `Naam`, `Leerlingnummer` FROM `Inkloktijd`")
        info = cur.fetchall()

        state = open("update.txt", "r")
        text = state.read()
        if text == "Yes":
            state.close()
            state = open("update.txt", "w")
            try:
                tree.delete(*tree.get_children())
                print("hallo")
            except:
                None

            print(info)

            for i in range(0, len(info)):
                print(i)
                tree.insert("", i, text=i+1, values = ((info[i])[0], (info[i])[1]))

            state.write("No")
            state.close()
            root.after(1000, update)
                

        else:
            state.close()
            root.after(1000, update)
                
    tree.pack()
    root.after(1000, update)
    root.mainloop()

start()
