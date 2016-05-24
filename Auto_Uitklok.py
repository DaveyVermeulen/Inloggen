import time
import pymysql
import decimal
from easygui import *
from datetime import datetime

#connect database
db = pymysql.connect(host="proxy50.weaved.com", port=38031, user="python", passwd="admin", db="inklokken")

#werkt als cursor
cur = db.cursor()   

def uitKlok():
    x = 1
    query = cur.execute("SELECT * FROM `inkloktijd` WHERE id = (%s)", x)
    
    while query:
        leerling = cur.fetchone()
        ln = leerling[1]
        tijdIn = leerling[3]
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
    if secmid == 33000: #9:15
        uitKlok()
    if secmid == 36000: #10:00
        uitKlok()
    if secmid == 38700: #10:45
        uitKlok()
    if secmid == 42600: #11:50
        uitKlok()
    if secmid == 45300: #12:35
        uitKlok()
    if secmid == 49800: #13:50
        uitKlok()
    if secmid == 52500: #14:35
        uitKlok()
    if secmid == 55800: #15:30
        uitKlok()
    if secmid == 58500: #16:15
        uitKlok()

def trigger30():
    if secmid == 32400: #9:00
        uitKlok()
    if secmid == 34200: #9:30
        uitKlok()
    if secmid == 36000: #10:00
        uitKlok()
    if secmid == 38700: #10:45
        uitKlok()
    if secmid == 40500: #11:15
        uitKlok()
    if secmid == 42300: #11:45
        uitKlok()
    if secmid == 45900: #12:45
        uitKlok()
    if secmid == 47700: #13:15
        uitKlok()

while True:
    tijd = datetime.now()
    uur = tijd.hour
    minuut = tijd.minute
    seconde = tijd.second
    secmid = tijd.hour*3600 + tijd.minute*60 + tijd.second
    if antwoord == "verkort":
        trigger30()
    if antwoord == "basis":
        trigger45()
    time.sleep(1)
