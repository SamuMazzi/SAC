#!/usr/bin/python3

import json
from google.cloud import pubsub_v1, firestore

project_id = "es13marzosm"

publisher = pubsub_v1.PublisherClient()

db = firestore.Client()
# prossima volta prova con functions_framework
def on_document_write(data, context):
    path_parts = context.resource.split('/documents/')[1].split('/')
    if 'users' in path_parts:
        return  # we don't care about writes in user
    collection_path = path_parts[0]
    document_path = '/'.join(path_parts[1:])
    # affected_doc = db.collection(collection_path).document(document_path)

    cur_value = data["value"]
    user_car = cur_value['fields'].get("user")
    print(cur_value)
    db.collection('info').add(data)
    price = list(cur_value['fields']['price'].values())[0]
    model = cur_value['fields']['model']['stringValue']
    if user_car is None:
        return
    user_car = user_car.get('stringValue')
    # Giulia
    cars_stream = db.collection(collection_path).where(u'price', u'>', f'${price}').stream()
    topic_path = publisher.topic_path(project_id, model) #cur_value['make']+
    for car in cars_stream:
        user = car.get('user')
        if user is not None:
            data_out = {'user': user_car, 'new_price': price}
            publisher.publish(topic_path, json.dumps(data_out).encode('utf-8'))