#!/usr/bin/python3
from google.cloud import firestore
import datetime
import numpy as np

db = firestore.Client()

def get_docname():
    dt=datetime.datetime.now()
    docname=dt.strftime('%Y%m%d')
    return docname

def get_stats(v):
    return {
        'count': len(v),
        'avg': np.mean(v),
        'std': np.std(v),
        'min': np.min(v),
        'max': np.max(v),
    }

def get_data(data):
    doc=data['value']
    v=[float(doc['fields'][k]['doubleValue']) for k in doc['fields'].keys()]
    return v

def update_db(data, context):
    db = firestore.Client()
    stats = get_stats(get_data(data))
    docname = context.resource.split('/')[-1]
    db.collection('temperature_stats').document(docname).set(stats)
