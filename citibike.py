#Import "requests" package to retrieve data from Internet
import requests
#Allow pandas to import JSON data
from pandas.io.json import json_normalize
#Allow charts and plots
import matplotlib.pyplot as plt
#pandas
import pandas as pd
#Allow to create database
import sqlite3 as lite

#"get" function brings in all data from specified URL
r = requests.get('http://www.citibikenyc.com/stations/json')

#Normalize JSON data from key "stationBeanList", import into DataFrame "df"
##Note: "stations" was gotten by looking at keys from JSON and determining
##which was useful
df = json_normalize(r.json()['stationBeanList'])

#Create database
con = lite.connect('citi_bike.db')
cur = con.cursor()

#Create reference table
with con:
    cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )')

#a prepared SQL statement we're going to execute over and over again
sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

#for loop to populate values in the database
with con:
    for station in r.json()['stationBeanList']:
        #id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location)
        cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))
