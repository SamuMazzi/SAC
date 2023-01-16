#!/usr/bin/python3

from api import get_cars
from flask import Flask, render_template
from google.cloud import firestore

app = Flask(__name__)

# app.config['PUBSUB_VERIFICATION_TOKEN'] = os.environ['PUBSUB_VERIFICATION_TOKEN']

db = firestore.Client()

@app.route('/', methods=['GET'])
def home():
    cars = get_cars()
    return render_template('index.html', cars=cars)

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
