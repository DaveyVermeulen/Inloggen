#prototype 1


Leerlingen = {}
from datetime import datetime
import json
import time
 
print("Selecteer modus ('database' of 'inloggen')")
modus = input()
 
if (modus != "database" and modus != "inloggen"):
  print("ERROR: onbekende modus")
 
if modus == "database":
  ln = input("leerlingennummer: ")
  while ln:
    naam = input("Naam: ")
    Leerlingen[ln] = naam
    print("Druk op enter om op te slaan")
    ln = input("of vul een nieuw leerlingennummer in ")
  json.dump(Leerlingen, open("database.txt", 'w'))
  print("Aanmaken leerlingen-database voltooid")
  print("Systeem zal nu afsluiten")
 
 
elif modus == "inloggen":
  inlog = {}
  Leerlingen = json.load(open("database.txt"))
  ln = input("Vul je leerlingennummer in: ")
  while ln:
    naam = Leerlingen.get(ln, "None")
    if naam == "None":
      print("Leerling onbekend, probeer opnieuw")
    else:
      print("Welkom", naam)
    tijd = datetime.now()
    print("het is vandaag", '%s-%s' % (tijd.day, tijd.month))
    print("Tijd:", '%s:%s:%s' % (tijd.hour, tijd.minute, tijd.second))
    inlog[naam] = (tijd.hour*3600 + tijd.minute*60 + tijd.second)
    json.dump(inlog, open("inlogtijd.txt", 'w'))
    time.sleep(2)
    ln = input("Vul je leerlingennummer in: ")
  print("Systeem zal nu afsluiten")




#protoype 2



Leerlingen = {}
from datetime import datetime
import json
import time
print("Selecteer modus ('database' of 'inloggen' of 'setup')")
modus = input()
 
if (modus != "database" and modus != "inloggen" and modus!= "setup"):
  print("ERROR: onbekende modus")

if modus == "database":
  ln = input("leerlingennummer: ")
  json.load(open("database.txt"))
  while ln:
    dic = {"0":"0"}
    naam = input("Naam: ")
    Leerlingen[ln] = naam
    print("Druk op enter om op te slaan")
    ln = input("of vul een nieuw leerlingennummer in ")
  dic.update({ln:naam})
  print("Aanmaken leerlingen-database voltooid")
  print("Systeem zal nu afsluiten")
  
if modus == "setup":
  ln = input("type 0: ")
  while ln:
    naam = input("type 0: ")
    Leerlingen[ln] = naam
    break
  with open('database.txt', 'w') as fp:
    dic = {ln:naam}
    ln = input("type 0: ")
    json.dump(dic, fp)
  print("Aanmaken leerlingen-database voltooid")
  print("Systeem zal nu afsluiten")
  
if modus == "inloggen":
  inlog = {}
  Leerlingen = json.load(open("database.txt"))
  ln = input("Vul je leerlingennummer in: ")
  while ln:
    naam = Leerlingen.get(ln, "None")
    if naam == "None":
      print("Leerling onbekend, probeer opnieuw")
    else:
      print("Welkom", naam)
    tijd = datetime.now()
    print("het is vandaag", '%s-%s' % (tijd.day, tijd.month))
    print("Tijd:", '%s:%s:%s' % (tijd.hour, tijd.minute, tijd.second))
    inlog[naam] = (tijd.hour*3600 + tijd.minute*60 + tijd.second)
    json.dump(inlog, open("inlogtijd.txt", 'w'))
    time.sleep(2)
    ln = input("Vul je leerlingennummer in: ")
  print("Systeem zal nu afsluiten")

