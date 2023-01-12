#!/usr/bin/python3

import json
import os
from google.cloud import pubsub_v1, firestore

subscription_name=os.environ.get('SUBSCRIPTION_NAME') or 'Giulia'
project_id = os.environ['PROJECT_ID']

subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()
subscription_path = subscriber.subscription_path(project_id, subscription_name)

db = firestore.Client()

def callback(message):
    # print(f'Message received: {message}')
    message.ack()
    obj = json.loads(message.data.decode('utf-8'))
    print(obj)
    if not obj.get('id') or not obj.get('time'):
        print(obj)
    
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
    # Giulia
    cars_stream = db.collection(collection_path).where(u'price', u'>', f'${price}').stream()
    topic_path = publisher.topic_path(project_id, cur_value['model']) #cur_value['make']+
    for car in cars_stream:
        user = car.get('user')
        if user is not None:
            data_out = {'user': user_car, 'new_price': price}
            publisher.publish(topic_path, json.dumps(data_out).encode('utf-8'))


if __name__ == '__main__':
    pull=subscriber.subscribe(subscription_path, callback=callback)
    try:
        print('a')
        pull.result(timeout=30)
    except:
        print('b')
        pull.cancel()