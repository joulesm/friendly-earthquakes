import logging
import config
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def main_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.config.update(DEBUG=True,PROPAGATE_EXCEPTIONS=True,TESTING=True)
    logging.basicConfig(level=logging.DEBUG)

    app.run()
