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

def Rooster():
      msg= "Welk lesrooster wilt u gebruiken?"#msg die wordt gedisplayed
      keuze=["Verkort","Standaard"]  
      lesrooster=buttonbox(msg,choices=keuze) #zelfde als bij inloggen
      rooster = open("rooster.txt", 'w')#opent bestand waarin keuze rooster is opgeslagen
      if lesrooster == "Verkort":
          rooster.write("Verkort")
          rooster.close()
          beheerder()
      if lesrooster == "Standaard":
          rooster.write("Standaard")
          rooster.close()
          beheerder()
    
def tag():
      msg="Houdt uw pasje voor de scanner"
      title="Uw pasje aub"
      choices=["Gedaan", "Annuleren"]
      invoer=buttonbox(msg,title=title,choices=choices)
      if invoer == "Gedaan":
            text=open("tags.txt","r")
            global tag
            tag=text.read()
            text.close()
            if invoer == "Annuleren":
                  return

def Toevoegen():
      tag()
      msg = "Voer uw informatie in"
      title = "Leerling toevoegen"
      fieldNames = ["Leerlingnummer", "Naam", "Klas"]
      fieldValues = []  
      fieldValues = multenterbox(msg,title, fieldNames)
      Leerlingnummer = int(fieldValues[0])
      Naam = fieldValues[1]
      Klas = fieldValues[2]
      cur.execute("INSERT INTO `Students` (`Leerlingnummer` , `Naam` , `Klas`, `NFC_tag`) VALUES (%s, %s, %s, %s)" , (Leerlingnummer, Naam, Klas, tag))
      db.commit()
    
    
#Data bewerkings menu
def Databewerken():
    msg="Wat wilt u bewerken?"
    title="Data bewerken"
    keuze=["Pasje(s) bewerken","Leerlingnummer bewerken","Naam bewerken","Terug"]
    invoer=buttonbox(msg,title=title,choices=keuze)
    if invoer == "Pasje(s) bewerken":
        pasje()
    if invoer == "Leerlingnummer bewerken":
        ln()
    if invoer == "Naam bewerken":
        naam()
    if invoer == "Terug":
        beheerder()

#Pasje bewerk menu
def pasje():
    msg="Pasje kwijt?"
    title="Pasje kwijt?"
    keuze=["Ja","Nee"]
    invoer=buttonbox(msg,title=title,choices=keuze)
    while invoer == "Ja":
          msg="Voer het leerlingnummer in:"
          title="Leerlingnummer"
          invoer=enterbox(msg,title)
          #selecteer in DB de row van het leerlingnummer
          tag()
          #update tag column voor de row van het leerlingnummer
          msg="Wilt u nog een pasje aanpassen?"
          title="Nog een pasje?"
          keuze=["Ja","Nee"]
          invoer=buttonbox(msg,title=title,choices=keuze)
   
    Databewerken()
        
def studieuren():
    date = datetime.now().date()
    try:
        info = cur.execute("SELECT * FROM `Studie_uren` WHERE `Leerlingnummer` = (%s)", (Leerlingnummer))
        dataSU = cur.fetchone()
        Datum = dataSU[4]
        print(Datum)
        Studie_uren = dataSU[5]
        print(Studie_uren)
            
        if Datum == date:
            dagTotaal = round((decimal.Decimal(str(SU)) + Studie_uren), 1)
            cur.execute("UPDATE `Studie_uren` SET  `Studie_uren` = (%s) WHERE `Leerlingnummer` = (%s)"  %(dagTotaal, Leerlingnummer))
            db.commit()
            print("DEBUG 1")
                
        else:
            cur.execute("INSERT INTO `Studie_uren` (`Leerlingnummer` , `Naam`, `Klas`, `Datum`, `Studie_uren`) VALUES (%s, %s, %s, %s, %s)", (Leerlingnummer, Naam, Klas, date, SU))
            db.commit()
            print("DEBUG 2")
                
    except:
        cur.execute("INSERT INTO `Studie_uren` (`Leerlingnummer` , `Naam`, `Klas`, `Datum`, `Studie_uren`) VALUES (%s, %s, %s, %s, %s)", (Leerlingnummer, Naam, Klas, date, round((SU), 1)))
        db.commit()
        print("DEBUG 3")

    if cur.execute("SELECT `Tijd` FROM `Inkloktijd` WHERE `Leerlingnummer` = (%s)" , (Leerlingnummer)):
        tijdIn = cur.fetchone()[0]
        cur.execute("DELETE FROM `Inkloktijd` WHERE `Leerlingnummer` = (%s)", (Leerlingnummer))
        cur.execute("INSERT INTO `Logs`  (`Leerlingnummer`, `Naam`, `In/uitloggen`) VALUES (%s, %s, 'Uit')", (Leerlingnummer, Naam))
        tijdNu = datetime.now()
        secmid = tijdNu.hour*3600 + tijdNu.minute*60 + tijdNu.second
        SU = (secmid - tijdIn)/2700
        db.commit()
       
        if SU < 0.00555555556:
            return

        elif SU > 0.888888889:
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

def klok():
    try:
        text = open("tags.txt","r")
        global tag
        tag = text.read()
        os.remove("tags.txt")
        if tag == "18011818261440":
            beheerder()
        else:
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
            studieuren()
        
        
    except:
        return

while 1:
    klok()
    time.sleep(0.5)
