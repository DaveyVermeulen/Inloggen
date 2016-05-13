import pymysql

#connect database
db = pymysql.connect( host="localhost", user="root", passwd="raspberry", db="Students")

#werkt als cursor
cur = db.cursor()

#importeert alles van table logs
tableLogs =cur.execute("SELECT * FROM logs")

ln = input("leerlingnummer: ")

while ln:
    cur.execute("INSERT INTO `logs`  (`ln`) VALUES (%s)", (ln)) #voegt ln() in tabel logs
    db.commit() #slaat database op
    ln = input("leerlingnummer: ")


try:
    cur.
db.close() #sluit database
