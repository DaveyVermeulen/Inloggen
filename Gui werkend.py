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
        Databewerken()

def Toevoegen():
      while invoer == "Ja":
            tag()
            msg = "Voer uw informatie in"
            title = "Leerling toevoegen"
            fieldNames = ["Leerlingnummer", "Naam","Klas"]
            fieldValues = []  
            fieldValues = multenterbox(msg,title, fieldNames)
            Leerlingnummer = int(fieldValues[0])
            Naam= fieldValues[1]
            Klas = fieldValues[2]
      
            cur.execute("INSERT INTO `Students` (`Leerlingnummer` , `Naam` , `Klas`, `NFC_tag`) VALUES (%s, %s, %s, %s)" , (Leerlingnummer, Naam, Klas, tag))
            db.commit()
            
            msg="Wilt u nog een Leerling toevoegen"
            title="Nog een Leerling?"
            keuze=["Ja","Nee"]
            invoer=buttonbox(msg,title=title,choices=keuze)
      

      
    
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

#leerlingnummer veranderen
def ln():
    msg="Naam leerling?"
    title="Veranderen leerlingnummer"
    naam=enterbox(msg,title)
    msg="Leerlingnummer leerling"
    title= "Veranderen leerlingnummer"
    leerlingnummer=enterbox(msg,title)
##selecteert row op basis van naam en update daar leerlingnummer
    msg="Nog een leerling aanpassen?"
    title="Veranderen leerlingnummer"
    choices=["Ja","Nee"]
    ja=buttonbox(msg, title=title,choices=choices)
    while ja == "Ja":
        msg="Nog een leerling aanpassen?"
        title="Veranderen leerlingnummer"
        choices=["Ja","Nee"]
        ja=buttonbox(msg, title=title,choices=choices)

    Databewerken()
    
def naam():
    def ln():
        msg="Leerlingnummer leerling?"
        title="Veranderen naam"
        leerlingnummer=enterbox(msg,title)
        msg="Naam leerling?"
        title= "Veranderen naam"
        naam=enterbox(msg,title)
##selecteer row op basis van leerlingnummer en update daar naam
        msg="Nog een leerling aanpassen?"
        title="Veranderen naam"
        choices=["Ja","Nee"]
        ja=buttonbox(msg, title=title,choices=choices)
        while ja == "Ja":
            msg="Nog een leerling aanpassen?"
            title="Veranderen naam"
            choices=["Ja","Nee"]
            ja=buttonbox(msg, title=title,choices=choices)
        Databewerken()
    
def beheerder():
    msg="Wat wilt u doen?"
    title="Beheerder"
    image="logo_school.gif"
    keuze=["Leerling(en) toevoegen","Data bewerken","Rooster veranderen","Terug"]
    wat=buttonbox(msg,title=title,image=image,choices=keuze)
    
    #Leerlingen toevoegen
    if wat == "Leerling(en) toevoegen":
        Toevoegen()
    if wat =="Data bewerken":
        Databewerken()
    if wat == "Rooster veranderen":
        Rooster()
    if wat == "Terug":
          print ("test") #moet inlog script starten
          
            
beheerder()
