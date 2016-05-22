import pymysql
import time
import decimal
from datetime import datetime

#connect database
db = pymysql.connect(host="proxy53.yoics.net", port=32388, user="python", passwd="admin", db="inklokken")

#werkt als cursor
cur = db.cursor()

def(inklokken):
        ln = input("leerlingnummer: ")

        nummer = 1

        while ln:
                if  cur.execute("SELECT `tijd` FROM `inkloktijd` WHERE `ln` = (%s)" , (ln)):
                    tijdIn = cur.fetchone()[0]
                    cur.execute("DELETE FROM `inkloktijd` WHERE `ln` = (%s)", (ln))
                    cur.execute("SELECT `Naam` FROM `students` WHERE `ln` = (%s)" , (ln))
                    Naam = cur.fetchone()[0]
                    cur.execute("SELECT `Studie_uren` FROM `students` WHERE `ln` = (%s)" , (ln))
                    studieUren = cur.fetchone()[0]
                    tijdNu = datetime.now()
                    secmid = tijdNu.hour*3600 + tijdNu.minute*60 + tijdNu.second
                    SU = (secmid - tijdIn)/2700
                    totaal = round((decimal.Decimal(str(SU)) + studieUren), 1)
                    cur.execute("UPDATE `students` SET `Studie_uren` = (%s) WHERE `ln`= (%s)" %(totaal, ln))
                    db.commit()
                    print("Je bent uitgeklokt,", Naam)
                    print("Je hebt", totaal, "studie-uren")
            
                else:
                    tijdNu = datetime.now()
                    tijd = tijdNu.hour*3600 + tijdNu.minute*60 + tijdNu.second
                    cur.execute("INSERT INTO `inkloktijd`  (`id`, `ln`, `tijd`) VALUES (%s, %s, %s)", (nummer, ln, tijd))
                    cur.execute("SELECT `Naam` FROM `students` WHERE `ln` = (%s)" , (ln))
                    Naam = cur.fetchone()[0]
                    db.commit()
                    print("Je bent ingeklokt,", Naam)
                nummer = nummer + 1
                ln = input("leerlingnummer: ")

db.close() #sluit database

print("Systeem beindigd")
