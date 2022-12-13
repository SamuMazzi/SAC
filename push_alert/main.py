import base64
import json
import os
import datetime
from flask import Flask, render_template, request
from google.cloud import firestore
# gcloud pubsub subscriptions create $SUBSCRIPTION_NAME --topic $TOPIC2 --push-endpoint "https://$PROJECT_ID.appspot.com/pubsub/push?token=$TOKEN" --ack-deadline 10

app = Flask(__name__)

app.config['PUBSUB_VERIFICATION_TOKEN'] = os.environ['PUBSUB_VERIFICATION_TOKEN']

db = firestore.Client()

def save_to_db(data):
    dt=datetime.datetime.fromtimestamp(data['message'])
    docname=dt.strftime('%Y%m%d')
    db.collection('temperature_alert').document(docname).set({str(data['timestamp']): 'alert'}, merge=True)

@app.route('/pubsub/push', methods=['POST'])
def pubsub_push():
    if requests.args.get('token', '') != app.config['PUBSUB_VERIFICATION_TOKEN']:
        return 'Invalid request', 403
    envelope=json.loads(request.data.decode('utf-8'))
    base64_msg=base64.b64decode(envelope['message']['data'])
    save_to_db(json.loads(base64_msg))
    return 'OK', 200

if __name == '__main__':
    app.run(host='localhost', post=8080, debug=True)

# gcloud app deploy