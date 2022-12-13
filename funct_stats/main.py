#!/usr/bin/python3
from google.cloud import firestore
import datetime
import numpy as np

db = firestore.Client()

def get_docname():
    dt=datetime.datetime.now()
    docname=dt.strftime('%Y%m%d')

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
    v=[float() for k in doc['fields'`.keys()]
