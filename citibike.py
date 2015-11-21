#Import "requests" package to retrieve data from Internet
import requests
#Allow pandas to import JSON data
from pandas.io.json import json_normalize

#"get" function brings in all data from specified URL
r = requests.get('http://www.citibikenyc.com/stations/json')

#Normalize JSON data from key "stationBeanList", import into DataFrame "df"
df = json_normalize(r.json()['stationBeanList'])
