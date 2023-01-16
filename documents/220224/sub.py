#!/usr/bin/python3

import json
import os
from google.cloud import pubsub_v1, firestore

project_id = os.environ['es220224sm']

subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()
subscription_path1 = subscriber.subscription_path(project_id, 'irrigazione')
subscription_path2 = subscriber.subscription_path(project_id, 'umidita')

db = firestore.Client()

def get_prenot(date):
    path = ('prenotazioni', date)
    return db.document(*path).get().to_dict()

def callback_irr(message):
    # print(f'Message received: {message}')
    message.ack()
    obj = json.loads(message.data.decode('utf-8'))
    time = obj.get('time')
    if not time:
        return 404
    print(f'Got irrigazione for {time} seconds')

def callback_umid(message):
    # print(f'Message received: {message}')
    message.ack()
    obj = json.loads(message.data.decode('utf-8'))
    umidita = obj.get('umidita')
    if not umidita:
        return 404
    print(f'Got irrigazione per umidità: {umidita}')
    

if __name__ == '__main__':
    pull1=subscriber.subscribe(subscription_path1, callback=callback_irr)
    pull2=subscriber.subscribe(subscription_path2, callback=callback_umid)
    try:
        pull1.result(timeout=30)
        pull2.result(timeout=30)
    except:
        pull1.cancel()
        pull2.cancel()