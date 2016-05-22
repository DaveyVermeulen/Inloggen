import time
import pymysql
import decimal
from easygui import *
from datetime import datetime


#connect database
db = pymysql.connect(host="proxy50.weaved.com", port=38031, user="python", passwd="admin", db="inklokken")

#werkt als cursor
cur = db.cursor()

def klok():
    ln = input("leerlingnummer: ")

    nummer = 1

    while ln:
        if  cur.execute("SELECT `tijd` FROM `inkloktijd` WHERE `ln` = (%s)" , (ln)):
            tijdIn = cur.fetchone()[0]
            cur.execute("DELETE FROM `inkloktijd` WHERE `ln` = (%s)", (ln))
            cur.execute("SELECT `Naam` FROM `students` WHERE `ln` = (%s)" , (ln))
            Naam = cur.fetchone()[0]
            cur.execute("INSERT INTO `logs`  (`ln`, `Naam`, `In/uitloggen`) VALUES (%s, %s, 'Uit')", (ln, Naam))
            cur.execute("SELECT `Studie_uren` FROM `students` WHERE `ln` = (%s)" , (ln))
            studieUren = cur.fetchone()[0]
            tijdNu = datetime.now()
            secmid = tijdNu.hour*3600 + tijdNu.minute*60 + tijdNu.second
            SU = (secmid - tijdIn)/2700
            if SU > 2400:
                totaal = studieUren + 1
                cur.execute("UPDATE `students` SET `Studie_uren` = (%s) WHERE `ln`= (%s)" %(totaal, ln))
            else:
                totaal = round((decimal.Decimal(str(SU)) + studieUren), 1)
                cur.execute("UPDATE `students` SET `Studie_uren` = (%s) WHERE `ln`= (%s)" %(totaal, ln))
            db.commit()
            print("Je bent uitgeklokt,", Naam)
            print("Je hebt", totaal, "studie-uren")
            
        elif cur.execute("SELECT `Naam` FROM `students` WHERE `ln` = (%s)" , (ln)):
            tijdNu = datetime.now()
            tijd = tijdNu.hour*3600 + tijdNu.minute*60 + tijdNu.second
            Naam = cur.fetchone()[0]
            cur.execute("INSERT INTO `logs`  (`ln`, `Naam`, `In/uitloggen`) VALUES (%s, %s, 'In')", (ln, Naam))
            cur.execute("INSERT INTO `inkloktijd`  (`id`, `ln`, `Naam`, `tijd`) VALUES (%s, %s, %s, %s)", (nummer, ln, Naam, tijd))
            db.commit()
            print("Je bent ingeklokt,", Naam)

        else:
            if "BEHEER":
                print("hier komt beheer functie")
            else:
                cur.execute("INSERT INTO `logs` (`ln`, `Naam`) VALUES (0, 'Onbekend')")
                db.commit()
                print("Sorry, deze leerling komt niet voor in de database")
            
        nummer = nummer + 1
        ln = input("leerlingnummer: ")

    db.close() #sluit database
    print("Systeem beindigd")
    
