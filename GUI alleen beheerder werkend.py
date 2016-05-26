from easygui import *
from time import sleep

def beheerder():
    msg="Wat wilt u doen?"
    title="Beheerder"
    keuze=["Leerling(en) toevoegen","Data bewerken","Rooster veranderen"]
    wat=buttonbox(msg,title=title,choices=keuze)
    
    #Leerlingen toevoegen
    if wat == "Leerlingen(en) toevoegen":
        Toevoegen()
    if wat =="Data bewerken":
        Databewerken()
def tag():
    msg="Houdt uw pasje voor de scanner"
    title="Uw pasje aub"
    choices=["Gedaan", "Annuleren"]
    invoer=buttonbox(msg,title=title,choices=choices)
    if invoer == "Gedaan":
        text=open("tags.txt","r")
        tag=text.read()
    if invoer == "Annuleren":
        return
        
        
def Toevoegen():
    msg = "Voer de informatie van de leerling in:"
    title = "Leerling informatie"
    waardes = ["Naam","Leerlingnummer","Klas",]
    invoer = []  
    invoer = multenterbox(msg,title, waardes)
    while 1:
        if invoer == None: break
        errmsg = ""
        for i in range(len(invoer)):
            if invoer[i].strip() == "":
                errmsg = errmsg + ('"%s" is een verplichte invoer.\n\n' % waardes[i])
        if errmsg == "": break # no problems found
        invoer = multenterbox(errmsg, title, waardes, invoer)
    for i in range(len(invoer)):
        #waardes uit list naar mysql schrijven.
        print("debug")
    tag()
    #schrijf de tag naar de rij
        

#data bewerkings menu
def Databewerken():
    msg="Wat wilt u bewerken?"
    title="Data bewerken"
    keuze=["Pasje(s) bewerken","Leerlingnummer bewerken","Naam bewerken"]
    invoer=buttonbox(msg,title=title,choices=keuze)
    if invoer == "Pasje(s) bewerken":
        pasje()
    if invoer == "Leerlingnummer bewerken":
        ln()

#Pasje bewerk menu
def pasje():
    msg="Pasje kwijt?"
    title="Pasje kwijt?"
    keuze=["Ja","Nee"]
    invoer=buttonbox(msg,title=title,choices=keuze)
    
    while invoer == "Ja":
        msg="Voer het leerlingnummer in:"
        title="Leerlingnummer"
        invoer=enterbox(msg,title=title)
        #selecteer in DB de row van het leerlingnummer
        msgbox("Houdt het pasje voor de scanner")
        #update tag column voor de row van het leerlingnummer
        msg="Wilt u nog een pasje aanpassen?"
        title="Nog een pasje?"
        keuze=["Ja","Nee"]
        invoer=buttonbox(msg,title=title,choices=keuze)
   
    return()

#leerlingnummer veranderen
def ln():
    msg="Leerlingnummer of Naam"
    title="Veranderen leerlingnummer"
    choices=["Leerlingnummer","Naam"]
    uitvoer=buttonbox(msg,title=title,choices=choices)
    if uitvoer == "Leerlingnummer":
        msgbox("hi")
    if uitvoer == "Naam":
        msgbox("hi")
            
beheerder()
