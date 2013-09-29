from pymongo import MongoClient

import config
import logging
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object(config)

conn = MongoClient(app.config['LOCAL_MONGO_URL'])
db = conn.fearthquakes


@app.route('/')
def main_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.config.update(DEBUG=True,PROPAGATE_EXCEPTIONS=True,TESTING=True)
    logging.basicConfig(level=logging.DEBUG)

    app.run()
