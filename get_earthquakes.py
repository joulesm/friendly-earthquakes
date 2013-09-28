import json, requests

url = 'http://comcat.cr.usgs.gov/fdsnws/event/1/query'
values = {'format': 'geojson',
          'starttime': '2013-09-28T23:00:00'}
          
earthquakes = requests.get(url, params=values).content

print earthquakes