from easygui import *
import time
import pymysql
import sys
import decimal
from datetime import datetime

def  beheerder():
    msg = "Inloggen of registreren?"
    title = "Beheerder  Menu"
    keuzes= ["Beheerder inloggen","Beheerder registreren"]
    out = buttonbox(msg,choices=keuzes)
    print (out)

def inloggen():
    msg= "Verkort lesrooster of niet?"
    keuze=["Verkort","Normaal"]
    tijd = datetime.now()
    uur = tijd.hour
    minuut = tijd.minute
    seconde = tijd.second
    secmid = tijd.hour*3600 + tijd.minute*60 + tijd.second
    
    inl=buttonbox(msg,choices=keuze)
    
    if inl == "Verkort":
        trigger30()
    if inl == "Normaal":
        trigger40()
    time.sleep(1)
    
def uitKlok():
    #connect database
    db = pymysql.connect(host="proxy50.weaved.com", port=38031, user="python", passwd="admin", db="inklokken")

    #werkt als cursor
    cur = db.cursor()
    x = 1

    text = open("beheer.txt", 'r')
    verkort = beheer.read()
    
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

def trigger30():
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
keuze = ["Inloggen","Beheerder","Afsluiten"]
antwoord = buttonbox(msg,image= plaatje, choices= keuze ) #Laat venster zien en geeft input terug

print(antwoord)
if antwoord == "Beheerder":
    beheerder()
if antwoord == "Inloggen":
   inloggen()
if antwoord == "Afsluiten":
    exit
    



