from easygui import *
import time
import pymysql
import sys
import decimal
import threading
from datetime import datetime

def beheer():
    print("Merge beheer van github" )
    
def rooster():
    file = open("rooster.txt", 'r')
    rooster = file.read()
    print(rooster)
    if rooster == "Verkort":
        while True:
            trigger30()
            time.sleep(1)
    if rooster == "Standaard":
        while True:
            trigger45()
            time.sleep(1)
        
    
def uitKlok():
    #connect database
    db = pymysql.connect(host="localhost", port=3141, user="python", passwd="admin", db="inklokken")

    #werkt als cursor
    cur = db.cursor()
    x = 1
 
    query = cur.execute("SELECT * FROM `Inkloktijd` WHERE id = (%s)", x)
    
    while query:
        leerling = cur.fetchone()
        Leerlingnummer = leerling[1]
        tijdIn = leerling[3]
        cur.execute("DELETE FROM `Inkloktijd` WHERE `Leerlingnummer` = (%s)", (Leerlingnummer))
        cur.execute("SELECT * FROM `Students` WHERE `Leerlingnummer` = (%s)" , (Leerlingnummer))
        data = cur.fetchone()
        Naam = data[1]
        studieUren = data[2]
        tijdNu = datetime.now()
        secmid = tijdNu.hour*3600 + tijdNu.minute*60 + tijdNu.second
        SU =(secmid - tijdIn)/2700
        if SU > 2400:
            totaal = studieUren + 1
            cur.execute("UPDATE `Students` SET `Studie_uren` = (%s) WHERE `Leerlingnummer`= (%s)" %(totaal, Leerlingnummer))
        else:
            totaal = round((decimal.Decimal(str(SU)) + studieUren), 1)
            cur.execute("UPDATE `Students` SET `Studie_uren` = (%s) WHERE `Leerlingnummer`= (%s)" %(totaal, Leerlingnummer))
        db.commit()
        x = x + 1
        query = cur.execute("SELECT * FROM `Inkloktijd` WHERE id = (%s)", x)
        
def trigger45():
    tijd = datetime.now()
    secmid = tijd.hour*3600 + tijd.minute*60 + tijd.second
    while secmid:
        if secmid == 33000:
            uitKlok()
        if secmid == 36000:
            uitKlok()
        if secmid == 38700:
            print("debug")
            uitKlok()
        if secmid == 39900:
            uitKlok()
        if secmid == 42600:
            uitKlok()
        if secmid == 45300:
            uitKlok()
        if secmid == 47100:
            uitKlok()
        if secmid == 49800:
            uitKlok()
        if secmid == 52500:
            uitKlok()
        if secmid == 55800:
            uitKlok()
        if secmid == 58500:
            uitKlok()
            time.sleep(58000)
            
        time.sleep(1)
        tijd = datetime.now()
        secmid = tijd.hour*3600 + tijd.minute*60 + tijd.second

def trigger30():
    tijd = datetime.now()
    secmid = tijd.hour*3600 + tijd.minute*60 + tijd.second
    while secmid:
        if secmid == 32400:
             uitKlok()
        if secmid == 34200:
            uitKlok()
        if secmid == 36000:
            uitKlok()
        if secmid == 36900:
            uitKlok()
        if secmid == 38700:
            uitKlok()
        if secmid == 40500:
            uitKlok()
        if secmid == 42300:
            uitKlok()
        if secmid == 44100:
            uitKlok()
        if secmid == 45900:
            uitKlok()
        if secmid == 47700:
            uitKlok()
            time.sleep(59500)
            
        time.sleep(1)
        tijd = datetime.now()
        secmid = tijd.hour*3600 + tijd.minute*60 + tijd.second
        

           
plaatje = "logo.gif"
msg = "Welke modus wilt u?"
keuze = ["Inloggen","Beheer","Afsluiten"]
antwoord = buttonbox(msg,image= plaatje, choices= keuze ) #Laat venster zien en geeft input terug

print(antwoord)
if antwoord == "Beheer":
    beheer()
if antwoord == "Inloggen":
    rooster()
if antwoord == "Afsluiten":
    exit("Systeem sluit af")
    
