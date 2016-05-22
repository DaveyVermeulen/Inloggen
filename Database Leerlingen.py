import pymysql
import time

#connect database
db = pymysql.connect(host="proxy52.yoics.net", port=37960, user="python", passwd="admin", db="inklokken")

#werkt als cursor
cur = db.cursor()

ln = input("leerlingnummer: ")

while ln:
        if  cur.execute("SELECT `Naam` FROM `students` WHERE `ln` = (%s)" , (ln)):
            ln = cur.fetchone()
            print(ln)
            
        else:
            print("Onbekende leerling")
            time.sleep(1)
            Naam = input("Naam: ")
            NFC_tag = input("NFC_tag: ")
            cur.execute("INSERT INTO `students`  (`ln`, `Naam`, `NFC_tag`) VALUES (%s, %s, %s)", (ln, Naam, NFC_tag))
            db.commit()
        ln = input("leerlingnummer: ")
db.close() #sluit database
