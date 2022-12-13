#!/usr/bin/python3

import time
from datetime import datetime
import json
import os
from google.cloud import pubsub_v1, firestore

subscription_name=os.environ['SUBSCRIPTION_NAME']
project_id = os.environ['PROJECT_ID']

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_name)

db = firestore.Client()

def save_temperature(data):
    dt=datetime.datetime.fromtimestamp(data['message'])
    docname=dt.strftime('%Y%m%d')
    db.collection('temperature').document(docname).set({str(data['timestamp']): data['temperature']}, merge=True)

def callback(message):
    # print(f'Message received: {message}')
    message.ack()
    try:
        save_temperature(json.loads(message.data.decode('utf-8')))
    except:
        pass

topic_name=os.environ['TOPIC']
topic_name2=os.environ['TOPIC2']
project_id=os.environ['PROJECT_ID']

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)
topic_path2 = publisher.topic_path(project_id, topic_name2)
# /sys/class/thermal/thermal_zone0/temp



if __name__ == '__main__':
    pull=subscriber.subscribe(subscription_path, callback=callback)
    try:
        pull.result(timeout=30)
    except:
        pull.cancel()