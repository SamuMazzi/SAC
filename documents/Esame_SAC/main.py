#!/usr/bin/python3

from datetime import datetime, timedelta
from flask import Flask, render_template
from google.cloud import firestore
from api import get_last_consumi,get_consumo, interpol
import calendar

app = Flask(__name__)

db = firestore.Client()
bollette_coll = db.collection('bollette')

def prev_mese(date: datetime):
    first = date.replace(day=1)
    last_month = first - timedelta(days=1)
    return last_month

def last_12_months():
    out = []
    date = datetime.now()
    for i in range(12):
        first = date.replace(day=1)
        last_month = first - timedelta(days=1)
        date = last_month.replace(day=1)
        out.append(date.strftime("%m-%Y"))
    return out


def get_c(date: datetime):
    out = get_consumo(date.strftime("%d-%m-%Y"))
    print(date)
    if out is None:
        out = interpol(date)
        print(out)
    return out

def get_c_mese(date: datetime):
    out = []
    out_c = []
    last_d = get_last_consumi(1, date)
    last_d_of_prev_prev_month = prev_mese(date)
    while len(last_d[0]) > 0 and last_d[0][0] >= last_d_of_prev_prev_month:
        c = last_d[1][0]
        d = last_d[0][0]
        out_c.append(c)
        out.append(d.strftime('%d-%m-%Y'))
        last_d = get_last_consumi(1, d)
    return out, out_c

def get_bolletta_mese(mese: str):
    prev_month = prev_mese(datetime.strptime(mese, '%m-%Y'))
    last_d_of_prev_prev_month = prev_mese(prev_month)
    info = get_c_mese(prev_month)
    datas_prev = info[0]
    costi = info[1]
    ref = {
        'prev': prev_month.strftime("%m-%Y"),
        'costo': (get_c(prev_month) - get_c(last_d_of_prev_prev_month))*0.5,
        'last_lect': datas_prev[0] if len(datas_prev) > 0 else "Nessuna data precedente", # get_last_consumi(1, datetime.now()),
        'consumi': costi # [interpol(prev), interpol(prev_mese(prev))]
    }
    return ref


@app.route('/details/<mese>', methods=['GET'])
def details(mese):
    bolletta = get_bolletta_mese(mese)
    return render_template('details.html', bolletta=bolletta)

@app.route('/', methods=['GET'])
def home():
    elenco = last_12_months()
    # cur_d_fn(1693526400)
    return render_template('index.html', bollette=elenco)

# 1693526400
def cur_d_fn(cur_date):
    date = datetime.fromtimestamp(cur_date)
    next_m = date + timedelta(days=calendar.monthrange(date.year,date.month)[1])
    m = next_m.strftime('%m-%Y')
    datas = get_bolletta_mese(m)
    bollette_coll.document(m).set(datas)


def on_document_create(data, context):
    cur_date = int(data["value"]["fields"]["date"]["doubleValue"])
    cur_d_fn(cur_date)

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)

"""
gcloud functions deploy on_document_create --runtime=python39 --trigger-event="providers/cloud.firestore/eventTypes/document.create" --trigger-resource="projects/esame20230116sm/databases/(default)/documents/letture/{lettura}"
"""