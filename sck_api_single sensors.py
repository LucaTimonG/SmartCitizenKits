# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 14:49:43 2020

@author: lucagreif
"""

import pandas as pd
import requests
import os, time
from datetime import date, timedelta
import csv

pfad = os.getcwd()

zeitraum = (open('zeitraum.txt', 'r'))
intervall = open('intervall.txt', 'r')
with open('kits.txt') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    kits = next(reader)
zeitraum = int(zeitraum.read())
intervall = int(intervall.read())
sensoren = ['113', '112', '14', '10', '53', '58', '89', '88', '87', '56', '55']
with open('sensors.txt') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    sensoren = next(reader)

enddf = pd.DataFrame()
now = date.today()
past = now - timedelta(days = zeitraum)

#functions_________________________________________________________________________________________
#Dataframe erstellen
def get_data (kit_id):

    for s in sensoren:  
        enddf = pd.DataFrame()
        url = "https://api.smartcitizen.me/v0/devices/"+i+"/readings?sensor_id="+s+"&rollup=" + str(intervall) + "h&from="+str(past)+"&to="+str(now)
        liste = []
        date_liste = []

        response = requests.get(url)
        data = response.json()      
        df = pd.DataFrame.from_dict(data) 

        for j in df.readings:
            wert = j[1]
            date = j[0]
            liste.append(wert)    
            date_liste.append(date)
                       
        series = pd.Series(liste)
        date_series = pd.Series(date_liste)
        spalte = (data['sensor_key'])            
        enddf['Date'] = date_series        
        enddf[str(spalte)] = series                          
        enddf.to_csv(str(s)+" "+str(spalte)+" "+str(i)+"Data.csv", sep=';')
        
        
        
        if str(response) == "<Response [200]>":
            print("Der " + str(spalte) + " Sensor des Kit Nr. " + str(i) + " wurde dem DataFrame hinzugefügt")

      
        time.sleep(1)

#final________________________________________________________________________    
for i in kits:
    kit_id=i
    get_data(i)

print("Die Daten der Geräte " + str(kits) + " wurden für die letzten " + str(zeitraum) + " Tage im " + str(intervall) + " Stunden Takt heruntergeladen")
print('Fertig, vielen Dank!')