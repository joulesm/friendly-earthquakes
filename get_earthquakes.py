import json, requests, datetime
import config
from pymongo import MongoClient, GEOSPHERE, GEO2D
from bson.son import SON

conn = MongoClient(config.LOCAL_MONGO_URL)
db = conn.fearthquakes

def get_earthquakes():
    url = 'http://comcat.cr.usgs.gov/fdsnws/event/1/query'
    time = (datetime.datetime.utcnow() - datetime.timedelta(minutes=90)).isoformat().split('.')[0]
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

def save_earthquakes(eqs):
    for eq in eqs['features']:
        earthquake = eq['properties']
        earthquake['id'] = eq['id']
        earthquake['geometry'] = eq['geometry']
        
        lon = earthquake['geometry']['coordinates'][0]
        lat = earthquake['geometry']['coordinates'][1]
        risky_list = db.friends.find( { "coords" :
            { "$near" :
                { "$geometry" :
                    SON(
                    { "type" : "Point" ,
                        "$maxDistance" : 1000.0,
                        "coordinates" : [ lon, lat ] }) }
                        
                        } } )
        id_list = [i['fb_id'] for i in risky_list]
        earthquake['risky_list'] = id_list
            
        db.earthquakes.save(earthquake)

if __name__ == "__main__":
    db.friends.ensure_index([("coords", GEO2D)])
    eq = get_earthquakes()
    print get_latlong(eq)
    save_earthquakes(eq)