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
    
@app.route('/alert_risky_people', methods = ['POST'])
def alert_risky_people():
    d = (datetime.datetime.utcnow() - datetime.timedelta(minutes=30)).isoformat(split('.'))[0]
    earthquake_list = db.earthquakes.find({"time" : {"$lt" : d}})
    for eq in earthquake_list:
        for risky_id in eq.risky_list:
            users_list = db.users.find( { "friends" : risky_id } )
            # ALERT USER
    
@app.route('/get_risky_friends', methods = ['POST'])
def get_risky_friends():
    user_data = json.loads(request.form['user'])
    friend_id_list = db.users.find({'fb_id': user_data['user']['fb_id']})
    d = (datetime.datetime.utcnow() - datetime.timedelta(minutes=30)).isoformat(split('.'))[0]
    earthquake_list = db.earthquakes.find({"time" : {"$lt" : d}})
    response = []
    for eq in earthquake_list:
        temp_risky_friend_list = []
        for risky_id in eq.risky_list:
            if risky_id in friend_id_list:
                temp_risky_friend_list.append(risky_id)
        if temp_risky_friend_list:
            friend_object_list = db.friends.find({"fb_id": {"$in": temp_risky_friend_list}})
            response.append((eq, friend_object_list)) 
    
if __name__ == '__main__':
    app.config.update(DEBUG=True,PROPAGATE_EXCEPTIONS=True,TESTING=True)
    logging.basicConfig(level=logging.DEBUG)

    app.run()
