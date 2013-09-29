import json, requests, datetime

def get_earthquakes():
    url = 'http://comcat.cr.usgs.gov/fdsnws/event/1/query'
    time = (datetime.datetime.utcnow() - datetime.timedelta(minutes=30)).isoformat().split('.')[0]
    values = {'format': 'geojson',
              'starttime': time}
              
    earthquakes = requests.get(url, params=values).content
    return json.loads(earthquakes)

def get_latlong(eq):
    eqData = []
    for feature in eq['features']:
        place = feature['properties']['place']
        lon = feature['geometry']['coordinates'][0]
        lat = feature['geometry']['coordinates'][1]
        mag = feature['properties']['mag']
        print place + "- longitude: " + str(lon) + " , latitude: " + str(lat) + " , magnitude: " +str(mag)
        eqData.append((lon, lat, mag))
    return eqData

if __name__ == "__main__":
    print get_latlong(get_earthquakes())