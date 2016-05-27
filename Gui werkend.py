from easygui import *
from time import sleep
        
def Rooster():
      msg= "Welk lesrooster wilt u gebruiken?"#msg die wordt gedisplayed
      keuze=["Verkort","Standaard"]  
      lesrooster=buttonbox(msg,choices=keuze) #zelfde als bij inloggen
      rooster = open("rooster.txt", 'w')#opent rooster
      if lesrooster == "Verkort":#als keuze verkort is run dit
          rooster.write("Verkort")
          rooster.close()
          beheerder()
      if lesrooster == "Standaard":#als keuze standaard is run dit
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
        tag=text.read()
    if invoer == "Annuleren":
        return()

def Toevoegen():
    msg = "Voer uw informatie in"
    title = "Leerling toevoegen"
    fieldNames = ["Leerlingnummer", "Naam", "Klas"]
    fieldValues = []  
    fieldValues = multenterbox(msg,title, fieldNames)

    while 1:
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" Dit is een vereist veld.\n\n' % fieldNames[i])
        if errmsg == "": break 
        fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
## uit fieldValues komt een list dus voeg die onderdelen in hun corrensponderende vak in de db
    msg="Nog een leerling toevoegen?"
    title="Leerlingen toevoegen"
    choices=["Ja","Nee"]
    ja=buttonbox(msg, title=title,choices=choices)
    while ja == "Ja":
        msg="Nog een leerling toevoegen?"
        title="Leerlingen toevoegen"
        choices=["Ja","Nee"]
        ja=buttonbox(msg, title=title,choices=choices)
    beheerder()
        

    
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
##naam is een str dus zoek die str in de naam column bij de db en selecteer in die row leerlingnummer update die met leerlingnummer
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
##leerlingnummer is een str dus zoek die str in de leerlingnummer column bij de db en selecteer in die row naam update die met naam
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
