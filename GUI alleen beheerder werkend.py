from easygui import *
from time import sleep
def  beheerder():
    msg = "Houdt uw pasje voor de scanner"
    title = "Beheerder inloggen"
    fieldNames = ["Name","Street Address","City","State","ZipCode"]
    fieldValues = []  # we start with blanks for the values
    fieldValues = multenterbox(msg,title, fieldNames)

    # make sure that none of the fields was left blank
    while 1:
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
        if errmsg == "": break
        fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
    
    print ("Reply was:", fieldValues)
plaatje = "logo_startpagina.gif"
msg = "Welke modus wilt u?"
keuze = ["Inloggen","Beheerder","Afsluiten","Test"]
antwoord = buttonbox(msg,image= plaatje, choices= keuze ) #Laat venster zien en geeft input terug

print(antwoord)
if antwoord == "Beheerder":
    beheerder()
    



