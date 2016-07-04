import os
import time
import pymysql
import decimal
from easygui import *
from datetime import datetime
import sys

#connect database
db = pymysql.connect(host="localhost", port=3141,  user="python", passwd="admin", db="inklokken")

#werkt als cursor
cur = db.cursor()

error = 0

def klok():
    try:
        text = open("/home/pi/Desktop/Inklokken/tags.txt","r")
        global tag
        tag = text.read()
        os.remove("/home/pi/Desktop/Inklokken/tags.txt")
        print(tag)
        cur.execute("SELECT * FROM `Leerlingen` WHERE (`NFC_tag` = (%s)) OR (`NFC_tag2` = (%s))" %(tag, tag))
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

    if Naam == "ADMIN":
        beheerder()
               
    else:
       if cur.execute("SELECT `Tijd` FROM `Inkloktijd` WHERE `Leerlingnummer` = (%s)" , (Leerlingnummer)):
           tijdIn = cur.fetchone()[0]
           tijdNu = datetime.now()
           secmid = tijdNu.hour*3600 + tijdNu.minute*60 + tijdNu.second
           global SU
           SU = (secmid - tijdIn)/2700

           if SU < 0.00555555556:
               return
        
           if SU > 0.888888889:
               SU = 1
               totaal = studieUren + 1
               cur.execute("DELETE FROM `Inkloktijd` WHERE `Leerlingnummer` = (%s)", (Leerlingnummer))
               cur.execute("INSERT INTO `Logs`  (`Leerlingnummer`, `Naam`, `In/uitloggen`) VALUES (%s, %s, 'Uit')", (Leerlingnummer, Naam))
               cur.execute("UPDATE `Leerlingen` SET `Studie_uren` = (%s) WHERE `Leerlingnummer`= (%s)" %(totaal, Leerlingnummer))
               db.commit()
               state = open("/home/pi/Desktop/Inklokken/update.txt", "w")
               state.write("Yes")
               state.close()
               studieuren()
           
          
           else:
               totaal = round((decimal.Decimal(str(SU)) + studieUren), 1)
               cur.execute("DELETE FROM `Inkloktijd` WHERE `Leerlingnummer` = (%s)", (Leerlingnummer))
               cur.execute("INSERT INTO `Logs`  (`Leerlingnummer`, `Naam`, `In/uitloggen`) VALUES (%s, %s, 'Uit')", (Leerlingnummer, Naam))
               cur.execute("UPDATE `Leerlingen` SET `Studie_uren` = (%s) WHERE `Leerlingnummer`= (%s)" %(totaal, Leerlingnummer))
               db.commit()
               state = open("/home/pi/Desktop/Inklokken/update.txt", "w")
               state.write("Yes")
               state.close()
               studieuren()
               
           print("Je bent uitgeklokt:", Naam)
           print("En je hebt", totaal, "studie-uren")
           time.sleep(1)
    
       elif cur.execute("SELECT `Naam` FROM `Leerlingen` WHERE `Leerlingnummer` = (%s)" , (Leerlingnummer)):
           tijdNu = datetime.now()
           tijd = tijdNu.hour*3600 + tijdNu.minute*60 + tijdNu.second
           Naam = cur.fetchone()[0]
           cur.execute("INSERT INTO `Logs`  (`Leerlingnummer`, `Naam`, `In/uitloggen`) VALUES (%s, %s, 'In')", (Leerlingnummer, Naam))
           cur.execute("INSERT INTO `Inkloktijd`  (`Leerlingnummer`, `Naam`, `Tijd`) VALUES (%s, %s, %s)", (Leerlingnummer, Naam, tijd))
           db.commit()
           state = open("/home/pi/Desktop/Inklokken/update.txt", "w")
           state.write("Yes")
           state.close()
           print("Je bent ingeklokt:", Naam)
    
       else:
           cur.execute("INSERT INTO `Logs` (`Leerlingnummer`, `Naam`) VALUES (0, 'Onbekend')")
           db.commit()
           state = open("/home/pi/Desktop/Inklokken/update.txt", "w")
           state.write("No")
           state.close()
           print("Sorry, deze leerling komt niet voor in de database")

    
    
def studieuren():       
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


def Rooster():
      msg= "Welk lesrooster wilt u gebruiken?"#msg die wordt gedisplayed
      keuze=["Verkort","Standaard"]  
      lesrooster=buttonbox(msg,choices=keuze) #zelfde als bij inloggen
      rooster = open("/home/pi/Desktop/Inklokken/rooster.txt", 'w')#opent bestand waarin keuze rooster is opgeslagen
      if lesrooster == "Verkort":
          rooster.write("Verkort")
          rooster.close()
          beheerder()
      if lesrooster == "Standaard":
          rooster.write("Standaard")
          rooster.close()
          beheerder()
    

def tag1():
    msg="Houdt het pasje voor de scanner"
    title="Uw pasje aub"
    choices=["Gedaan", "Annuleren"]
    invoer=buttonbox(msg,title=title,choices=choices)
    try:
        if invoer == "Gedaan":
            text=open("/home/pi/Desktop/Inklokken/tags.txt","r")
            global tagP
            tagP=text.read()
            text.close()
            os.remove("/home/pi/Desktop/Inklokken/tags.txt")
        
        if invoer == "Annuleren":
            error = 1
            beheerder()

        msg="Scan mobiele telefoon, klik op annuleren indien niet van toepassing"
        title="Mobiel"
        choices=["Gedaan", "Annuleren"]
        invoer=buttonbox(msg, title=title, choices=choices)
        try:
            if invoer == "Gedaan":
                text=open("/home/pi/Desktop/Inklokken/tags.txt", "r")
                global tagM
                tagM = text.read()
                text.close()
                os.remove("/home/pi/Desktop/Inklokken/tags.txt")

            else:
                global error
                error = "cancel"

        except:
            msg="Geen telefoon gevonden"
            title="Geen telefoon gevonden"
            msgbox=(msg, title)
            error = "cancel"
    except:
        msg="Geen pasje gevonden"
        title="Geen pasje gevonden"
        msgbox(msg,title=title)
        beheerder()         


def Toevoegen():
    tag1()
    msg = "Voer uw informatie in"
    title = "Leerling toevoegen"
    fieldNames = ["Leerlingnummer", "Naam", "Klas"]
    fieldValues = []
    fieldValues = multenterbox(msg,title, fieldNames)
    if fieldValues == None:
        beheerder()
    else:
        Leerlingnummer = fieldValues[0]
        Naam = fieldValues[1]
        Klas = fieldValues[2]
        if error == "cancel":
            cur.execute("INSERT INTO `Leerlingen` (`Leerlingnummer` , `Naam` , `Klas`, `NFC_tag`) VALUES (%s, %s, %s, %s)"  ,(Leerlingnummer, Naam, Klas, tagP))
        else:
            cur.execute("INSERT INTO `Leerlingen` (`Leerlingnummer` , `Naam` , `Klas`, `NFC_tag`, `NFC_tag2`) VALUES (%s, %s, %s, %s, %s)"  ,(Leerlingnummer, Naam, Klas, tagP, tagM))
        db.commit()
        msg = Naam+" is toegevoegd aan de database"
        title = "Leerling toegevoegd"
        msgbox(msg,title=title)
        beheerder()
      

def Verwijderen():
    msg="Vul het leerlingnummer in"
    title="Verwijderen"
    invoer=enterbox(msg,title=title)

    if invoer == None:
        return
    else:
        try:
            cur.execute("SELECT `Naam` FROM `Leerlingen` WHERE `Leerlingnummer` = (%s)", (invoer))
            naam= cur.fetchone()[0]
            msg="Wilt u de leerling: "+naam+" verwijderen uit de database?"
            title="Leerling verwijderen"
            choices=["Ja", "Nee"]
            invoer=buttonbox(msg,title=title, choices=choices)
            if invoer == "Ja":
                cur.execute("DELETE FROM `Leerlingen` WHERE `Leerlingnummer` = (%s)", (invoer))
                db.commit()
                msg="De leerling "+naam+" is verwijderd"
                title="Leerling verwijderd"
                msgbox(msg, title)
            
            else:
                msg="De leerling "+naam+" is niet verwijderd"
                title="Leerling behouden"
                msgbox(msg, title)  
        
        except:
            msg=invoer+" is niet bekend in de database"
            title='onbekend leerlingnummer'
            msgbox(msg, title=title)
        
        beheerder()

    
def beheerder():
    msg="Wat wilt u doen?"
    title="Beheerder"
    image="/home/pi/Desktop/Inklokken/logo_school.gif"
    keuze=["Leerling toevoegen","Leerling verwijderen","Rooster veranderen","Terug","Aflsuiten"]
    what=buttonbox(msg,title=title,image=image,choices=keuze)
    
    #Leerlingen toevoegen
    if what == "Leerling toevoegen":
        Toevoegen()
    if what =="Leerling verwijderen":
        Verwijderen()
    if what == "Rooster veranderen":
        Rooster()
    if what == "Terug":
        print("return")  
    if what == "Aflsuiten":
        sys.exit()
        
        
    
def run():
    while 1:
        klok()
        time.sleep(0.5)

print("Sluit dit command venster om het programma af te sluiten")
run()
