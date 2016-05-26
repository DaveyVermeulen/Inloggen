from easygui import *
from time import sleep
def beheerder:
    msg="Wat wilt u doen?"
    title="Beheerder"
    keuze=["Leerling(en) toevoegen","Data bewerken","Rooster veranderen"]
    wat=buttonbox(msg,title=title,choices=keuze)
    if wat == "Leerlingen(en) toevoegen":
        #wachten op pasje
        if #wachten op pasje == true
            msg = "Voer de informatie van de leerling in:"
            title = "Credit Card Application"
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
            print "Informatie is:", invoer
    if wat =="Data bewerken":
        msg="Wat wilt u bewerken?"
        title="Data bewerken"
        keuze=["Pasje(s) bewerken","Leerlingnummer bewerken","Naam bewerken"]
        
        
    


if tag =
    



