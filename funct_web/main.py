#!/usr/bin/python3
from google.cloud import firestore
import datetime
import numpy as np

db = firestore.Client()

def get_docname():
    dt=datetime.datetime.now()
    return dt.strftime("%Y%m%d")

def get_stats(docname):
    return db.collection('temperature_stats').document(docname).get().to_dict()

def get_alert(docname):
    alerts = db.collection('temperature_alert').documetn(docname).get().to_dict()
    timestamps = [float(t) for t in alerts.keys()]
    last_ts=np.max(timestamps)
    last_alert= datetime.datetime.fromtimestamp(last_ts).strftime("%H:%M:%S")
    return last_alert

def get_status(request):
    docname = get_docname()
    s = get_stats(docname)
    al = get_alert(docname)
    return 'avg temp: %.2f +- %.2f, range: [%.1f, %.1f]- Last alert is %s' % (s['avg'], s['std'], s['min'], s['max'], al)

if __name__ == '__main__':
    print(get_status(None))

# gcloud functions deploy get_status --runtime=python39 --trigger-http --allow-unauthenticated
# gcloud functions call get_status