#!/usr/bin/env python

import time
import pymysql
import sys
import decimal
from datetime import datetime

#connect database
db = pymysql.connect(host="proxy53.yoics.net", port=32388, user="python", passwd="admin", db="inklokken")

#werkt als cursor
cur = db.cursor()

def uitKlok():
    x = 1
    query = cur.execute("SELECT * FROM `inkloktijd` WHERE id = (%s)", x)
    
    while query:
        leerling = cur.fetchone()
        ln = leerling[1]
        tijdIn = leerling[2]
        print(tijdIn)
        cur.execute("DELETE FROM `inkloktijd` WHERE `ln` = (%s)", (ln))
        cur.execute("SELECT * FROM `students` WHERE `ln` = (%s)" , (ln))
        data = cur.fetchone()
        Naam = data[1]
        studieUren = data[2]
        print(studieUren)
        tijdNu = datetime.now()
        secmid = tijdNu.hour*3600 + tijdNu.minute*60 + tijdNu.second
        SU = (secmid - tijdIn)/2700
        print(SU)
        totaal = round((decimal.Decimal(str(SU)) + studieUren), 1)
        cur.execute("UPDATE `students` SET `Studie_uren` = (%s) WHERE `ln`= (%s)" %(totaal, ln))
        db.commit()
        x = x + 1
        query = cur.execute("SELECT * FROM `inkloktijd` WHERE id = (%s)", x)
        
def trigger45():
    if secmid == 33000:
        uitKlok()
    if secmid == 36000:
        uitKlok()
    if secmid == 38700:
        uitKlok()
    if secmid == 42600:
        uitKlok()
    if secmid == 45300:
        uitKlok()
    if secmid == 49800:
        uitKlok()
    if secmid == 52500:
        uitKlok()
    if secmid == 55800:
        uitKlok()
    if secmid == 58500:
        uitKlok()
        sys.exit("Einde lesdag")
        

while True:
  tijd = datetime.now()
  uur = tijd.hour
  minuut = tijd.minute
  seconde = tijd.second
  secmid = tijd.hour*3600 + tijd.minute*60 + tijd.second
  trigger45()
  time.sleep(1)
