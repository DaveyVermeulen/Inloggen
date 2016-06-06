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
        global tag
        tag = text.read()
        os.remove("tags.txt")
        print(tag)
        cur.execute("SELECT * FROM `Students` WHERE `NFC_tag` = (%s)", (tag))
        data = cur.fetchone()
        print(data)
        global Leerlingnummer
        Leerlingnummer = data[0]
        global Naam
        Naam = data[1]
        global studieUren
        studieUren = data[2]
        global Klas
        Klas = data[3]
        
        
    except:
        return


    def studieuren():
        date = datetime.now().date()
        try:
            info = cur.execute("SELECT * FROM `Studie_uren` WHERE (`Leerlingnummer` = (%s) AND `Datum` = (%s))" %(Leerlingnummer, date))
            dataSU = cur.fetchone()
            print(dataSU)
            Datum = dataSU[4]
            print("mySQL:", Datum)
            print("Python:", date)
            Studie_uren = dataSU[5]
            print(Studie_uren)

            dagTotaal = round((decimal.Decimal(str(SU)) + Studie_uren), 1)
            cur.execute("UPDATE `Studie_uren` SET  `Studie_uren` = (%s) WHERE `Leerlingnummer`, `Datum` = (%s, %s)"  %(dagTotaal, Leerlingnummer, date))
            db.commit()
                
        except:
            cur.execute("INSERT INTO `Studie_uren` (`Leerlingnummer` , `Naam`, `Klas`, `Datum`, `Studie_uren`) VALUES (%s, %s, %s, %s, %s)", (Leerlingnummer, Naam, Klas, date, round((decimal.Decimal(str(SU))), 1)))
            db.commit()



        
                                       
    if cur.execute("SELECT `Tijd` FROM `Inkloktijd` WHERE `Leerlingnummer` = (%s)" , (Leerlingnummer)):
       tijdIn = cur.fetchone()[0]
       tijdNu = datetime.now()
       secmid = tijdNu.hour*3600 + tijdNu.minute*60 + tijdNu.second
       SU = (secmid - tijdIn)/2700
              
       if SU < 0.00555555556:
           return

       if SU > 0.888888889:
           totaal = studieUren + 1
           cur.execute("DELETE FROM `Inkloktijd` WHERE `Leerlingnummer` = (%s)", (Leerlingnummer))
           cur.execute("INSERT INTO `Logs`  (`Leerlingnummer`, `Naam`, `In/uitloggen`) VALUES (%s, %s, 'Uit')", (Leerlingnummer, Naam))
           cur.execute("UPDATE `Students` SET `Studie_uren` = (%s) WHERE `Leerlingnummer`= (%s)" %(totaal, Leerlingnummer))
           db.commit()
           studieuren()
           
          
       else:
           totaal = round((decimal.Decimal(str(SU)) + studieUren), 1)
           cur.execute("DELETE FROM `Inkloktijd` WHERE `Leerlingnummer` = (%s)", (Leerlingnummer))
           cur.execute("INSERT INTO `Logs`  (`Leerlingnummer`, `Naam`, `In/uitloggen`) VALUES (%s, %s, 'Uit')", (Leerlingnummer, Naam))
           cur.execute("UPDATE `Students` SET `Studie_uren` = (%s) WHERE `Leerlingnummer`= (%s)" %(totaal, Leerlingnummer))
           db.commit()
           studieuren()
           
       print("Je bent uitgeklokt:", Naam)
       print("En je hebt", totaal, "studie-uren")
            
    elif cur.execute("SELECT `Naam` FROM `Students` WHERE `Leerlingnummer` = (%s)" , (Leerlingnummer)):
        tijdNu = datetime.now()
        tijd = tijdNu.hour*3600 + tijdNu.minute*60 + tijdNu.second
        Naam = cur.fetchone()[0]
        cur.execute("INSERT INTO `Logs`  (`Leerlingnummer`, `Naam`, `In/uitloggen`) VALUES (%s, %s, 'In')", (Leerlingnummer, Naam))
        cur.execute("INSERT INTO `Inkloktijd`  (`Leerlingnummer`, `Naam`, `Tijd`) VALUES (%s, %s, %s)", (Leerlingnummer, Naam, tijd))
        db.commit()
        print("Je bent ingeklokt:", Naam)

    else:
        cur.execute("INSERT INTO `Logs` (`Leerlingnummer`, `Naam`) VALUES (0, 'Onbekend')")
        db.commit()
        print("Sorry, deze leerling komt niet voor in de database")
            
        
while 1:
    
    klok()
    time.sleep(0.5)
    
db.close() #sluit database
print("Systeem beindigd")
    

