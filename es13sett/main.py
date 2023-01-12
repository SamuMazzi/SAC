from flask import Flask, render_template
from google.cloud import firestore

# TODO: Testare se, se chiamo API con dati diversi da queli segnati mi da errore lui in automatico o se devo gestire io errori

app = Flask(__name__)

# app.config['PUBSUB_VERIFICATION_TOKEN'] = os.environ['PUBSUB_VERIFICATION_TOKEN']

db = firestore.Client()

def add_to_slot_if_empty(slot: int, new_data):
    path = ('slots', str(slot))
    if get_slot(slot) is not None:
        return False

    db.document(*path).set(new_data)
    return True

def get_doc_slot(slot: int):
    path = ('slots', str(slot))
    return db.document(*path)

def get_slot(slot: int):
    return get_doc_slot(slot).get().to_dict()
   

def _get_labels():
    out = []
    for i in range(10):
        data = get_slot(i)
        if data is not None:
            out.append(data)
    return out


def handle_below_minimum(data, context):
    if data['quantity'] < data['minimum']:
        db.collection('richieste').add({
            'label': data['label'],
            'quantity': 6
        })


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