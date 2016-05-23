from easygui import *
import time
import pymysql
import sys
import decimal
import threading
from datetime import datetime

def beheer():
    msg = "Inloggen of registreren?"#msg die wordt gedisplayed
    title = "Beheerder  Menu" #title van box
    keuzes= ["Rooster", "Beheerder inloggen","Beheerder registreren"] #maakt list die easygui naar knoppen omzet
    out = buttonbox(msg,choices=keuzes) #keuze box werkt zoals een input functie
    print (out) #debug
    if out == "Rooster": #vraagt of de input van the box Rooster was
        msg= "Welk lesrooster wilt u gebruiken?"#msg die wordt gedisplayed
        keuze=["Verkort","Standaard"]  
        lesrooster=buttonbox(msg,choices=keuze) #zelfde als bij inloggen
        rooster = open("rooster.txt", 'w')#opent rooster
        if lesrooster == "Verkort":#als keuze verkort is run dit
            rooster.write("Verkort")
            rooster.close()
        if lesrooster == "Standaard":#als keuze standaard is run dit
            rooster.write("Standaard")
            rooster.close()
    if out == "Beheerder registeren":# nog niet af maar kom registreren van beheerder
        msg=msgbox("Vul uw gegevens in AUB")
        

def rooster(): #checkt wat de waarde is van rooster en dan runt het bijhorende rooster
    file = open("rooster.txt", 'r')
    rooster = file.read()
    print(rooster)
    if rooster == "Verkort":
        while True:
            trigger30()
            time.sleep(1)
    if rooster == "Standaard":
        trigger45()
            
    
def uitKlok():#inloggen bij database en uitloggen van leerlingen na trigger van roosters
    #connect database
    db = pymysql.connect(host="proxy50.weaved.com", port=38031, user="python", passwd="admin", db="inklokken")

    #werkt als cursor
    cur = db.cursor()
    x = 1
 
    query = cur.execute("SELECT * FROM `inkloktijd` WHERE id = (%s)", x) #vraagt eerste line op van table inklok
    
    while query:
        leerling = cur.fetchone() #convert naar tuple in python
        ln = leerling[1]
        tijdIn = leerling[3]
        cur.execute("DELETE FROM `inkloktijd` WHERE `ln` = (%s)", (ln)) #verwijdert leerling uit table inklok
        cur.execute("SELECT * FROM `students` WHERE `ln` = (%s)" , (ln)) #vraagt alle informatie op uit table students
        data = cur.fetchone()
        Naam = data[1]
        studieUren = data[2]
        tijdNu = datetime.now()
        secmid = tijdNu.hour*3600 + tijdNu.minute*60 + tijdNu.second #aantal seconden sinds middernacht
        SU =(secmid - tijdIn)/2700 #berekent aantal seconden van in tot uitklok
        if SU > 2400:
            totaal = studieUren + 1
            cur.execute("UPDATE `students` SET `Studie_uren` = (%s) WHERE `ln`= (%s)" %(totaal, ln))
        else:
            totaal = round((decimal.Decimal(str(SU)) + studieUren), 1)
            cur.execute("UPDATE `students` SET `Studie_uren` = (%s) WHERE `ln`= (%s)" %(totaal, ln))
        db.commit()
        x = x + 1
        query = cur.execute("SELECT * FROM `inkloktijd` WHERE id = (%s)", x) #gaat verder in table inklok, nu bij line x = x + 1
        
def trigger45():
    tijd = datetime.now() # geeft tijd vanaf systeem
    secmid = tijd.hour*3600 + tijd.minute*60 + tijd.second #seconden vanaf middernacht
    while secmid:
        if secmid == 33000:#als tijd is einde lesuur, klok dan iedereen uit
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
            sys.exit("Einde lesdag")#systeem sluit, niemand kan weer inklokken
        time.sleep(1)#iedere seconde wordt gecheckt of het al tijd is(einde van het uur)
        tijd = datetime.now()
        secmid = tijd.hour*3600 + tijd.minute*60 + tijd.second

def trigger30(): # voor uitleg naar trigger45, nog niet geheel omgeschreven
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

           
plaatje = "logo_startpagina.gif"#plaatje van school logo
msg = "Welke modus wilt u?"
keuze = ["Inloggen","Beheer","Afsluiten"]
antwoord = buttonbox(msg,image= plaatje, choices= keuze ) #Laat venster zien en geeft input terug

print(antwoord)#debug
if antwoord == "Beheer":#checkt wat het antwoord is
    beheer()#eerder gedefined
if antwoord == "Inloggen":
    rooster()#eerder gedefined
if antwoord == "Afsluiten":
    exit("Systeem sluit af")
    
