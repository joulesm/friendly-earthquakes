from main import db
import json
from bson.son import SON

SF = [37.759881,-122.437392]

risky_list = db.friends.find( { "coords" : SON({"$maxDistance": 10.0 , "$near": SF })  }) 
print risky_list.count
print json.dumps([[i['name'], i['coords']] for i in risky_list])