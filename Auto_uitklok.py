from easygui import *
import time
import pymysql
import sys
import decimal
from datetime import datetime

try:
    import Scripts as kx
except:
    from Inklokken import Scripts as kx
    
def rooster():
    file = open("/home/pi/Desktop/Inklokken/rooster.txt", 'r')
    rooster = file.read()
    print(rooster)
    if rooster == "Verkort":
        while True:
            trigger30()
            time.sleep(1)
    if rooster == "Standaard":
        while True:
            trigger45()
            time.sleep(1)
        
            
def trigger45():
    tijd = datetime.now()
    secmid = tijd.hour*3600 + tijd.minute*60 + tijd.second
    while secmid:
        if secmid == 33000:
            kx.uitKlok()
        if secmid == 36000:
            kx.uitKlok()
        if secmid == 38700:
            kx.uitKlok()
        if secmid == 39900:
            kx.uitKlok()
        if secmid == 42600:
            kx.uitKlok()
        if secmid == 45300:
            kx.uitKlok()
        if secmid == 47100:
            kx.uitKlok()
        if secmid == 49800:
            kx.uitKlok()
        if secmid == 52500:
            kx.uitKlok()
        if secmid == 55800:
            kx.uitKlok()
        if secmid == 58500:
            kx.uitKlok()
            time.sleep(58000)
            
        time.sleep(1)
        tijd = datetime.now()
        secmid = tijd.hour*3600 + tijd.minute*60 + tijd.second

def trigger30():
    tijd = datetime.now()
    secmid = tijd.hour*3600 + tijd.minute*60 + tijd.second
    while secmid:
        if secmid == 32400:
             kx.uitKlok()
        if secmid == 34200:
            kx.uitKlok()
        if secmid == 36000:
            kx.uitKlok()
        if secmid == 36900:
            kx.uitKlok()
        if secmid == 38700:
            kx.uitKlok()
        if secmid == 40500:
            kx.uitKlok()
        if secmid == 42300:
            kx.uitKlok()
        if secmid == 44100:
            kx.uitKlok()
        if secmid == 45900:
            kx.uitKlok()
        if secmid == 47700:
            kx.uitKlok()
            time.sleep(59500)
            
        time.sleep(1)
        tijd = datetime.now()
        secmid = tijd.hour*3600 + tijd.minute*60 + tijd.second
    
rooster()
