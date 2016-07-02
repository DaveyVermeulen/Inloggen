import pymysql
import time
from datetime import datetime
import decimal

def uitKlok():
    #connect database
    db = pymysql.connect(host="localhost", port=3141, user="python", passwd="admin", db="inklokken")

    #werkt als cursor
    cur = db.cursor()

    x = 1
    
    query = cur.execute("SELECT * FROM `Inkloktijd` WHERE id = (%s)", x)
    
    while query:       
        leerling = cur.fetchone()
        global Leerlingnummer
        Leerlingnummer = leerling[1]
        global tijdIn
        tijdIn = leerling[3]
        cur.execute("DELETE FROM `Inkloktijd` WHERE `Leerlingnummer` = (%s)", (Leerlingnummer))
        cur.execute("SELECT * FROM `Leerlingen` WHERE `Leerlingnummer` = (%s)" , (Leerlingnummer))
        data = cur.fetchone()
        global Naam
        Naam = data[1]
        global studieUren
        studieUren = data[2]
        global Klas
        Klas = data[3]
        tijdNu = datetime.now()
        secmid = tijdNu.hour*3600 + tijdNu.minute*60 + tijdNu.second
        global SU
        SU =(secmid - tijdIn)/2700
        if SU > 2400:
            totaal = studieUren + 1
            cur.execute("UPDATE `Leerlingen` SET `Studie_uren` = (%s) WHERE `Leerlingnummer`= (%s)" %(totaal, Leerlingnummer))
        else:
            totaal = round((decimal.Decimal(str(SU)) + studieUren), 1)
            cur.execute("UPDATE `Leerlingen` SET `Studie_uren` = (%s) WHERE `Leerlingnummer`= (%s)" %(totaal, Leerlingnummer))
        cur.execute("INSERT INTO `Logs`  (`Leerlingnummer`, `Naam`, `In/uitloggen`) VALUES (%s, %s, 'Uit')", (Leerlingnummer, Naam))
        cur.db.commit()
        db.close()
        studieuren()
        x = x + 1

        #connect database
        db = pymysql.connect(host="localhost", port=3141, user="python", passwd="admin", db="inklokken")

        #werkt als cursor
        cur = db.cursor()
        
        query = cur.execute("SELECT * FROM `Inkloktijd` WHERE id = (%s)", x)

    cur.execute("TRUNCATE `Inkloktijd`")
    text = open("/home/pi/Desktop/Inklokken/update.txt", "w")
    text.write("Yes")
    text.close()


def studieuren():
        db = pymysql.connect(host="localhost", port=3141, user="python", passwd="admin", db="inklokken")
        cur = db.cursor()
        
        cur.execute("SELECT * FROM `Leerlingen` WHERE `Leerlingnummer` = (%s)" , (Leerlingnummer))
        data = cur.fetchone()
        Naam = data[1]
        Klas = data[3]

        datenow = datetime.now().date()
        date = str(datenow)
        print(date)
        print(Leerlingnummer)
        try:
            cur.execute("SELECT * FROM `Studie_uren` WHERE `Leerlingnummer` = (%s)"  %(Leerlingnummer))
            info = cur.fetchall()
            length = len(info)
            Data = info[length-1]
            Studie_uren = Data[5]
            ID = Data[0]
            dagTotaal = round((SU + Studie_uren), 1)
            
            if Data[4]== date:
                cur.execute("UPDATE `Studie_uren` SET  `Studie_uren` = (%s) WHERE `id` = (%s)"  %(dagTotaal, ID))
                db.commit()
                
            else:
                cur.execute("INSERT INTO `Studie_uren` (`Leerlingnummer` , `Naam`, `Klas`, `Datum`, `Studie_uren`) VALUES (%s, %s, %s, %s, %s)", (Leerlingnummer, Naam, Klas, date, round((decimal.Decimal(str(SU))), 1)))
                db.commit()  
        except:
            cur.execute("INSERT INTO `Studie_uren` (`Leerlingnummer` , `Naam`, `Klas`, `Datum`, `Studie_uren`) VALUES (%s, %s, %s, %s, %s)", (Leerlingnummer, Naam, Klas, date, round((decimal.Decimal(str(SU))), 1)))
            db.commit()

        db.close()
