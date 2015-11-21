#Import "requests" package to retrieve data from Internet
import requests

#"get" function brings in all data from specified URL
r = requests.get('http://www.citibikenyc.com/stations/json')
