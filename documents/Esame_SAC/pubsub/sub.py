#!/usr/bin/python3

import json
import os
from google.cloud import pubsub_v1, firestore

subscription_name=os.environ['SUBSCRIPTION_NAME']
project_id = os.environ['PROJECT_ID']

subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()
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
    
def on_document_write(data, context):
    path_parts = context.resource.split('/documents/')[1].split('/')
    if 'users' in path_parts:
        return  # we don't care about writes in user
    collection_path = path_parts[0]
    document_path = '/'.join(path_parts[1:])
    # affected_doc = db.collection(collection_path).document(document_path)

    cur_value = data["value"]
    user_car = cur_value.get("user")
    price = cur_value['price']
    if user_car is None:
        return
    cars_stream = db.collection(collection_path).where(u'price', u'>', f'${price}').stream()
    topic_path = publisher.topic_path(project_id, cur_value['make']+cur_value['model'])
    for car in cars_stream:
        user = car.get('user')
        if user is not None:
            data_out = {'user': user_car, 'new_price': price}
            publisher.publish(topic_path, json.dumps(data_out).encode('utf-8'))


if __name__ == '__main__':
    pull=subscriber.subscribe(subscription_path, callback=callback)
    try:
        pull.result(timeout=30)
    except:
        pull.cancel()