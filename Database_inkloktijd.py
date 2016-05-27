import os
import time
import pymysql
import decimal
from easygui import *
from datetime import datetime


#connect database
db = pymysql.connect(host="localhost", port=3141,  user="python", passwd="admin", db="inklokken")

#werkt als cursor
cur = db.cursor()

def klok():
    try:
        text = open("tags.txt","r")
        tag = text.read()
        os.remove("tags.txt")
        print(tag)
        cur.execute("SELECT * FROM `Students` WHERE `NFC_tag` = (%s)", (tag))
        data = cur.fetchone()
        print(data)
        Leerlingnummer = data[0]
        Naam = data[1]
        studieUren = data[2]
        Klas = data[3]
        
        
    except:
        return


    def studieuren():
        date = datetime.now().date()
        try:
            info = cur.execute("SELECT * FROM `Studie_uren` WHERE `Leerlingnummer` = (%s)", (Leerlingnummer))
            Datum = cur.fetchone()[3]
            Studie_uren = cur.fetchone()[4]

            if Datum == date:
                dagTotaal = SU + Studie_uren
                cur.execute("UPDATE ` Studie_uren` SET `Studie_uren` = (%s) WHERE `Leerlingnummer` = (%s)" %(dagTotaal, Leerlingnummer))
            else:
                cur.execute("INSERT INTO `Studie_uren` (`Leerlingnummer` , `Naam`, `Klas`, `Datum`, `Studie_uren`) VALUES (%s, %s, %s, %s, %s)", (Leerlingnummer, Naam, Klas, date, SU)) 

        except:
            cur.execute("INSERT INTO `Studie_uren` (`Leerlingnummer` , `Naam`, `Klas`, `Datum`, `Studie_uren`) VALUES (%s, %s, %s, %s, %s)", (Leerlingnummer, Naam, Klas, date, SU))
            
        db.commit()
                            
    if cur.execute("SELECT `Tijd` FROM `Inkloktijd` WHERE `Leerlingnummer` = (%s)" , (Leerlingnummer)):
       tijdIn = cur.fetchone()[0]
       cur.execute("INSERT INTO `Logs`  (`Leerlingnummer`, `Naam`, `In/uitloggen`) VALUES (%s, %s, 'Uit')", (Leerlingnummer, Naam))
       tijdNu = datetime.now()
       secmid = tijdNu.hour*3600 + tijdNu.minute*60 + tijdNu.second
       SU = (secmid - tijdIn)/2700
              
       if SU < 15:
           return
       elif SU > 2400:
           totaal = studieUren + 1
           cur.execute("UPDATE `Students` SET `Studie_uren` = (%s) WHERE `Leerlingnummer`= (%s)" %(totaal, Leerlingnummer))
           studieuren()
          
       else:
           totaal = round((decimal.Decimal(str(SU)) + studieUren), 1)
           cur.execute("UPDATE `Students` SET `Studie_uren` = (%s) WHERE `Leerlingnummer`= (%s)" %(totaal, Leerlingnummer))
           studieuren()
           
       db.commit()
       print("Je bent uitgeklokt,", Naam)
       print("Je hebt", totaal, "studie-uren")
            
    elif cur.execute("SELECT `Naam` FROM `Students` WHERE `Leerlingnummer` = (%s)" , (Leerlingnummer)):
        tijdNu = datetime.now()
        tijd = tijdNu.hour*3600 + tijdNu.minute*60 + tijdNu.second
        Naam = cur.fetchone()[0]
        cur.execute("INSERT INTO `Logs`  (`Leerlingnummer`, `Naam`, `In/uitloggen`) VALUES (%s, %s, 'In')", (Leerlingnummer, Naam))
        cur.execute("INSERT INTO `Inkloktijd`  (`Leerlingnummer`, `Naam`, `Tijd`) VALUES (%s, %s, %s)", (Leerlingnummer, Naam, tijd))
        db.commit()
        print("Je bent ingeklokt,", Naam)

    else:
        cur.execute("INSERT INTO `Logs` (`Leerlingnummer`, `Naam`) VALUES (0, 'Onbekend')")
        db.commit()
        print("Sorry, deze leerling komt niet voor in de database")
            
        
while 1:
    klok()
    time.sleep(0.5)
    
db.close() #sluit database
print("Systeem beindigd")
    

