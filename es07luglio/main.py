from flask import Flask, render_template
from google.cloud import firestore

app = Flask(__name__)

# app.config['PUBSUB_VERIFICATION_TOKEN'] = os.environ['PUBSUB_VERIFICATION_TOKEN']

db = firestore.Client()

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
