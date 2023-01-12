#!/usr/bin/python3

from datetime import datetime
from google.cloud import firestore

def get_docname():
    dt=datetime.datetime.now()
    docname=dt.strftime('%Y%m%d')
    return docname

def get_data(data):
    doc=data['value']
    v=[float(doc['fields'][k]['doubleValue']) for k in doc['fields'].keys()]
    return v

def richiesta_comanda(nome):
    db.collection()

def update_db(data, context):
    db = firestore.Client()
    stats = get_stats(get_data(data))
    docname = context.resource.split[-1]
    db.collection('temperature_stts').document(docname).set(stats)