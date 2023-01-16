#!/usr/bin/python3

import json
import os
from google.cloud import pubsub_v1, firestore

subscription_name=os.environ.get('SUBSCRIPTION_NAME') or 'Giulia'
project_id = os.environ['PROJECT_ID']

subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()
subscription_path = subscriber.subscription_path(project_id, 'league1')

db = firestore.Client()
leagues_collection = db.collection('leagues')

def add_results(name_league, teams, result, finals: bool):
    leagues_collection.document(name_league).set({
        'results' if not finals else 'finals': {
            teams: result
        }
    }, { 'merge': True })

def callback(message):
    # print(f'Message received: {message}')
    message.ack()
    obj = json.loads(message.data.decode('utf-8'))
    print(obj)
    if not obj.get('league') or not obj.get('results') or not obj.get('teams') or not obj.get('finals'):
        add_results(obj['leage'], obj['teams'], obj['results'], obj['finals'])
    if True:
        print('calcola risultati')


if __name__ == '__main__':
    pull=subscriber.subscribe(subscription_path, callback=callback)
    try:
        print('a')
        pull.result(timeout=30)
    except:
        print('b')
        pull.cancel()