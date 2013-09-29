from pymongo import MongoClient

import config
import json
import logging
import datetime
import get_earthquakes as eq
from flask import Flask, render_template, request

app = Flask(__name__)
app.config.from_object(config)

conn = MongoClient(app.config['LOCAL_MONGO_URL'])
db = conn.fearthquakes

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/add_data', methods = ['POST'])
def add_data():
    client_data = json.loads(request.form['json_data'])
    friend_ids = map(lambda x: x['fb_id'], client_data['friends'])
    client_data['user']['friends'] = friend_ids
    db.users.update({'fb_id': client_data['user']['fb_id']}, client_data['user'], upsert=True)
    for friend in client_data['friends']:
        db.friends.update({'fb_id': friend['fb_id']}, friend, upsert=True)
    return "Success!"
    
# @app.route('/get_risky_friends', methods = ['POST']))
# def get_risky_friends():
#     d = (datetime.datetime.utcnow() - datetime.timedelta(minutes=30)).isoformat(split('.')[0]
#     earthquake_list = db.earthquakes.find("time" : {"$lt" : d})
#     for eq in earthquake_list:
#         lon = eq['geometry']['coordinates'][0]
#         lat = eq['geometry']['coordinates'][1]
#         risky_list = db.friends.find( { "coords" :
#                          { "$near" :
#                             { "$geometry" :
#                                 { "type" : "Point" ,
#                                   "coordinates" : [ lon, lat ] } },
#                               "$maxDistance" : 100000
#                       } } )
#         id_list = [i[fb_id] for i in risky_list]
#         for risky_id in id_list:
#             users_list = db.users.find( { "friends" : risky_id } )

if __name__ == '__main__':
    app.config.update(DEBUG=True,PROPAGATE_EXCEPTIONS=True,TESTING=True)
    logging.basicConfig(level=logging.DEBUG)

    app.run()
