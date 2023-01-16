#!/usr/bin/python3

from api import get_plants
from flask import Flask, render_template, request
from google.cloud import firestore
from datetime import datetime
import json

app = Flask(__name__)

# app.config['PUBSUB_VERIFICATION_TOKEN'] = os.environ['PUBSUB_VERIFICATION_TOKEN']

db = firestore.Client()

@app.route('/pubsub/push', methods=['POST'])
def pubsub_push():
    obj=json.loads(request.data.decode('utf-8'))
    time = obj.get('time')
    umidita = obj.get('umidita')
    if not time and not umidita:
        return '', 404
    print(f'Got irrigazione for {time} seconds')
    print(f'Got irrigazione per umidità: {umidita}')
    db.collection('data').add(obj)
    return 'OK', 200

@app.route('/', methods=['GET'])
def home():
    out = {}
    plants_info = {}
    plants = get_plants()
    for plant in plants:
        for data_semina, num_semina in plant['semina']:
            data_vera = datetime.strptime(data_semina, '%Y-%m-%d').date()
            time_between = data_vera - datetime.now()
            obj = {
                    'name': plant['plant']['name'],
                    'num': num_semina
                }
            if time_between.days < 0:
                out['past'] = obj
            elif time_between.days < 10:
                out['prox'] = obj
            elif time_between.days > 10:
                out['far'] = obj
        plants_info[plant['plant']['name']] = plant['plant']

    return render_template('index.html', plants_semina=out, plants_info=plants_info)

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
