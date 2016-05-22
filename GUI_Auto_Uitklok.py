from easygui import *
import time
import pymysql
import sys
import decimal
import threading
from datetime import datetime

def beheer():
    msg = "Inloggen of registreren?"
    title = "Beheerder  Menu"
    keuzes= ["Rooster", "Beheerder inloggen","Beheerder registreren"]
    out = buttonbox(msg,choices=keuzes)
    print (out)
    if out == "Rooster":
        msg= "Welk lesrooster wilt u gebruiken?"
        keuze=["Verkort","Standaard"]  
        lesrooster=buttonbox(msg,choices=keuze)
        rooster = open("rooster.txt", 'w')
        if lesrooster == "Verkort":
            rooster.write("Verkort")
            rooster.close()
        if lesrooster == "Standaard":
            rooster.write("Standaard")
            rooster.close()

def rooster():
    file = open("rooster.txt", 'r')
    rooster = file.read()
    print(rooster)
    if rooster == "Verkort":
        while True:
            trigger30()
            time.sleep(1)
    if rooster == "Standaard":
        trigger45()
            
    
def uitKlok():
    #connect database
    db = pymysql.connect(host="proxy50.weaved.com", port=38031, user="python", passwd="admin", db="inklokken")

    #werkt als cursor
    cur = db.cursor()
    x = 1
 
    query = cur.execute("SELECT * FROM `inkloktijd` WHERE id = (%s)", x)
    
    while query:
        leerling = cur.fetchone()
        ln = leerling[1]
        tijdIn = leerling[3]
        cur.execute("DELETE FROM `inkloktijd` WHERE `ln` = (%s)", (ln))
        cur.execute("SELECT * FROM `students` WHERE `ln` = (%s)" , (ln))
        data = cur.fetchone()
        Naam = data[1]
        studieUren = data[2]
        tijdNu = datetime.now()
        secmid = tijdNu.hour*3600 + tijdNu.minute*60 + tijdNu.second
        SU =(secmid - tijdIn)/2700
        if SU > 2400:
            totaal = studieUren + 1
            cur.execute("UPDATE `students` SET `Studie_uren` = (%s) WHERE `ln`= (%s)" %(totaal, ln))
        else:
            totaal = round((decimal.Decimal(str(SU)) + studieUren), 1)
            cur.execute("UPDATE `students` SET `Studie_uren` = (%s) WHERE `ln`= (%s)" %(totaal, ln))
        db.commit()
        x = x + 1
        query = cur.execute("SELECT * FROM `inkloktijd` WHERE id = (%s)", x)
        
def trigger45():
    tijd = datetime.now()
    secmid = tijd.hour*3600 + tijd.minute*60 + tijd.second
    while secmid:
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
        time.sleep(1)
        tijd = datetime.now()
        secmid = tijd.hour*3600 + tijd.minute*60 + tijd.second

def trigger30():
    tijd = datetime.now()
    secmid = tijd.hour*3600 + tijd.minute*60 + tijd.second
    if secmid == 32400:
        uitKlok()
    if secmid == 34200:
        uitKlok()
    if secmid == 36000:
        uitKlok()
    if secmid == 38700:
        uitKlok()
    if secmid == 40500:
        uitKlok()
    if secmid == 42300:
        uitKlok()
    if secmid == 45900:
        uitKlok()
    if secmid == 47700:
        uitKlok()
        sys.exit("Einde lesdag")

           
plaatje = "logo_startpagina.gif"
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
    
