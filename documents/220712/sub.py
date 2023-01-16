#!/usr/bin/python3

from datetime import datetime
import json
import os
from google.cloud import pubsub_v1, firestore

subscription_name=os.environ['SUBSCRIPTION_NAME']
project_id = os.environ['PROJECT_ID']

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_name)

db = firestore.Client()

def get_prenot(date):
    path = ('prenotazioni', date)
    return db.document(*path).get().to_dict()

def callback(message):
    # print(f'Message received: {message}')
    message.ack()
    obj = json.loads(message.data.decode('utf-8'))
    if not obj.get('id') or not obj.get('time'):
        return 404
    times = ['08-10', '10-12', '12-14', '14-16', '16-18', '18-20']
    data = get_prenot(datetime.datetime().strftime('%Y-%m-%d'))
    hour = datetime.datetime().hour()
    for time in times:
        if (time.split('-')[0]) > hour and int(time.split('-')[1]) < hour:
            return "ok"
    try:
        save_temperature()
    except:
        pass

topic_name=os.environ['TOPIC']

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)


if __name__ == '__main__':
    pull=subscriber.subscribe(subscription_path, callback=callback)
    try:
        pull.result(timeout=30)
    except:
        pull.cancel()