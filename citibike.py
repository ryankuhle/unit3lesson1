import requests
from pandas.io.json import json_normalize
import pandas as pd
import sqlite3 as lite
import time
from dateutil.parser import parse
import collections



con = lite.connect('citi_bike.db')
cur = con.cursor()

### CREATE REFERENCE TABLE ###
#with con:
#    cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )')

#a prepared SQL statement we're going to execute over and over again
#sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

#for loop to populate values in reference table
#with con:
#    for station in r.json()['stationBeanList']:
        #id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location)
#        cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))

### CREATE BIKE STATUS TABLE ###
#station_ids = df['id'].tolist()
#station_ids = ['_' + str(x) + ' INT' for x in station_ids]
#with con:
#    cur.execute("CREATE TABLE available_bikes ( execution_time INT, " +  ", ".join(station_ids) + ");")

def activityStatus():
    #
    r = requests.get('http://www.citibikenyc.com/stations/json')
    df = json_normalize(r.json()['stationBeanList'])
    exec_time = parse(r.json()['executionTime'])
    print "Insert data at: %s" % exec_time
    with con:
        cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))
    id_bikes = collections.defaultdict(int) #defaultdict to store available bikes by station
    for station in r.json()['stationBeanList']:
        id_bikes[station['id']] = station['availableBikes']
    with con:
        for k, v in id_bikes.iteritems():
            cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")

t = 0

while t < 60:
    activityStatus()
    t += 1
    time.sleep(60)

print "Done! Thank you for your patience."
