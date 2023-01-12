import datetime
from flask import Flask, render_template, request
from google.cloud import firestore

# TODO: Testare se, se chiamo API con dati diversi da queli segnati mi da errore lui in automatico o se devo gestire io errori

app = Flask(__name__)

# app.config['PUBSUB_VERIFICATION_TOKEN'] = os.environ['PUBSUB_VERIFICATION_TOKEN']

db = firestore.Client()

def save_to_db(data):
    dt=datetime.datetime.fromtimestamp(data['message'])
    docname=dt.strftime('%Y%m%d')
    db.collection('temperature_alert').document(docname).set({str(data['timestamp']): 'alert'}, merge=True)

def add_plant_if_not_exist(date, plant, new_data):
    path = (date, plant)
    if get_plant(date, plant) is not None:
        return False

    db.document(*path).set(new_data)
    return True

def get_plant(date, plant):
    path = (date, plant)
    return db.document(*path).get().to_dict()

@app.route('/api/v1/garden/plant/<date>/<plant>', methods=['POST'])
def add_plant(date, plant):
    date_list = date.split('-')
    data = {
        'plant': {
            'name': 'coll',
            'sprout-time': '3 weeks',
            'full-growth': "3 months",
            'edible': True
        },
        'number': 6
    }
    try:
        data_json = request.json['PlantInfo']  #request.is_json() ? request.get_json()
        res = add_plant_if_not_exist(date, plant, data_json)
        if not res:
            return 'Conflict.', 409
        return 'Success.', 200
    except:
        return "Generic error.", 400

@app.route('/api/v1/garden/plant/<date>/<plant>', methods=['GET'])
def get_bottiglie(date, plant):
    try:
        data = get_plant(date, plant)
        return data, 200
    except:
        return 'Generic error.', 404

def _get_all_plants():
    out = []
    list_dates = db.collection('/').get()
    list_docs = db.get_all(list_dates)
    for doc in list_docs:
        doc.reference
        doc.to_dict()
    return out

@app.route('/api/v1/labels', methods=['GET'])
def get_labels():
    try:
        out = _get_labels()
        return out, 200
    except:
        return 'Generic error.', 404

@app.route('/api/v1/clean', methods=['GET'])
def clean():    
    return 'OK', 200

@app.route('/', methods=['GET'])
def home():
    labels = _get_labels()
    out = {}
    for label in labels:
        print(label)
        type_label = label['label']['type']
        if out.get(type_label) is not None:
            out[type_label].append(label)
        else:
            out[type_label] = [label]
    print(out)
    return render_template('index.html', labels=out)

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)

# gcloud app deploy